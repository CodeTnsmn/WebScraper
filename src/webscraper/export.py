import sqlite3

import pandas as pd

from webscraper import store

COLUMNS = ["hedef_adi", "zaman_damgasi", "ham_fiyat", "fiyat", "para_birimi", "stok_durumu"]


def _stock_label(in_stock: bool | None) -> str:
    if in_stock is None:
        return ""
    return "evet" if in_stock else "hayır"


def _export_dataframe(conn: sqlite3.Connection, target_id: int | None) -> pd.DataFrame:
    rows = store.get_snapshots_with_target_name(conn, target_id)
    records = [
        {
            "hedef_adi": row["target_name"],
            "zaman_damgasi": row["timestamp"].isoformat(),
            "ham_fiyat": row["raw_price"],
            "fiyat": str(row["price"]) if row["price"] is not None else "",
            "para_birimi": row["currency"],
            "stok_durumu": _stock_label(row["in_stock"]),
        }
        for row in rows
    ]
    return pd.DataFrame(records, columns=COLUMNS)


def export_csv(conn: sqlite3.Connection, path: str, *, target_id: int | None = None) -> None:
    _export_dataframe(conn, target_id).to_csv(path, index=False)


def export_excel(conn: sqlite3.Connection, path: str, *, target_id: int | None = None) -> None:
    _export_dataframe(conn, target_id).to_excel(path, index=False)
