import sqlite3
from datetime import datetime, timezone
from decimal import Decimal

from webscraper.models import PriceSnapshot, Target

_SCHEMA = """
CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    name_selector TEXT NOT NULL,
    price_selector TEXT NOT NULL,
    default_currency TEXT NOT NULL,
    stock_selector TEXT,
    stock_in_stock_text TEXT
);

CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    raw_price TEXT NOT NULL,
    price TEXT,
    currency TEXT NOT NULL,
    in_stock INTEGER
);
"""


def connect(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.executescript(_SCHEMA)
    return conn


def add_target(conn: sqlite3.Connection, target: Target) -> int:
    cursor = conn.execute(
        "INSERT INTO targets (name, url, name_selector, price_selector, default_currency, "
        "stock_selector, stock_in_stock_text) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            target.name,
            target.url,
            target.name_selector,
            target.price_selector,
            target.default_currency,
            target.stock_selector,
            target.stock_in_stock_text,
        ),
    )
    conn.commit()
    return cursor.lastrowid


def list_targets(conn: sqlite3.Connection) -> list[Target]:
    rows = conn.execute(
        "SELECT id, name, url, name_selector, price_selector, default_currency, "
        "stock_selector, stock_in_stock_text FROM targets ORDER BY id"
    ).fetchall()
    return [
        Target(
            id=row[0],
            name=row[1],
            url=row[2],
            name_selector=row[3],
            price_selector=row[4],
            default_currency=row[5],
            stock_selector=row[6],
            stock_in_stock_text=row[7],
        )
        for row in rows
    ]


def delete_target(conn: sqlite3.Connection, target_id: int) -> None:
    """Removes the target row only — existing snapshots are kept (domain.md rule)."""
    conn.execute("DELETE FROM targets WHERE id = ?", (target_id,))
    conn.commit()


def save_snapshot(conn: sqlite3.Connection, snapshot: PriceSnapshot) -> int:
    cursor = conn.execute(
        "INSERT INTO snapshots (target_id, timestamp, raw_price, price, currency, in_stock) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            snapshot.target_id,
            snapshot.timestamp.astimezone(timezone.utc).isoformat(),
            snapshot.raw_price,
            str(snapshot.price) if snapshot.price is not None else None,
            snapshot.currency,
            None if snapshot.in_stock is None else int(snapshot.in_stock),
        ),
    )
    conn.commit()
    return cursor.lastrowid


def get_snapshots_with_target_name(
    conn: sqlite3.Connection, target_id: int | None = None
) -> list[dict]:
    """Snapshots joined with their target's name, for export (LEFT JOIN keeps
    snapshots whose target was later deleted — domain.md: history outlives the target).
    """
    query = (
        "SELECT s.target_id, t.name, s.timestamp, s.raw_price, s.price, s.currency, s.in_stock "
        "FROM snapshots s LEFT JOIN targets t ON t.id = s.target_id"
    )
    params: tuple = ()
    if target_id is not None:
        query += " WHERE s.target_id = ?"
        params = (target_id,)
    query += " ORDER BY s.timestamp ASC"

    rows = conn.execute(query, params).fetchall()
    return [
        {
            "target_name": row[1] if row[1] is not None else f"(silinmiş hedef {row[0]})",
            "timestamp": datetime.fromisoformat(row[2]),
            "raw_price": row[3],
            "price": Decimal(row[4]) if row[4] is not None else None,
            "currency": row[5],
            "in_stock": None if row[6] is None else bool(row[6]),
        }
        for row in rows
    ]


def get_history(conn: sqlite3.Connection, target_id: int) -> list[PriceSnapshot]:
    rows = conn.execute(
        "SELECT id, target_id, timestamp, raw_price, price, currency, in_stock "
        "FROM snapshots WHERE target_id = ? ORDER BY timestamp ASC",
        (target_id,),
    ).fetchall()
    return [
        PriceSnapshot(
            id=row[0],
            target_id=row[1],
            timestamp=datetime.fromisoformat(row[2]),
            raw_price=row[3],
            price=Decimal(row[4]) if row[4] is not None else None,
            currency=row[5],
            in_stock=None if row[6] is None else bool(row[6]),
        )
        for row in rows
    ]
