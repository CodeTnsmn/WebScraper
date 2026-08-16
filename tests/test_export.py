import csv
from datetime import datetime, timezone
from decimal import Decimal

import pandas as pd

from webscraper import export, store
from webscraper.models import PriceSnapshot, Target


def _seeded_conn():
    conn = store.connect(":memory:")
    target_id = store.add_target(
        conn,
        Target(
            name="Kulaklık X200",
            url="http://example.test/product",
            name_selector=".t",
            price_selector=".p",
            default_currency="TRY",
        ),
    )
    store.save_snapshot(
        conn,
        PriceSnapshot(
            target_id=target_id,
            timestamp=datetime(2026, 8, 1, tzinfo=timezone.utc),
            raw_price="1.199,00 TL",
            price=Decimal("1199.00"),
            currency="TRY",
            in_stock=True,
        ),
    )
    store.save_snapshot(
        conn,
        PriceSnapshot(
            target_id=target_id,
            timestamp=datetime(2026, 8, 15, tzinfo=timezone.utc),
            raw_price="1.299,90 TL",
            price=Decimal("1299.90"),
            currency="TRY",
            in_stock=False,
        ),
    )
    return conn, target_id


def test_export_csv_row_count_and_columns_ac1(tmp_path):
    conn, target_id = _seeded_conn()
    out = tmp_path / "history.csv"

    export.export_csv(conn, str(out), target_id=target_id)

    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0]["hedef_adi"] == "Kulaklık X200"
    assert rows[0]["ham_fiyat"] == "1.199,00 TL"
    assert rows[0]["fiyat"] == "1199.00"
    assert rows[0]["para_birimi"] == "TRY"
    assert rows[0]["stok_durumu"] == "evet"
    assert rows[1]["stok_durumu"] == "hayır"


def test_export_excel_matches_csv_ac2(tmp_path):
    conn, target_id = _seeded_conn()
    csv_path = tmp_path / "history.csv"
    xlsx_path = tmp_path / "history.xlsx"

    export.export_csv(conn, str(csv_path), target_id=target_id)
    export.export_excel(conn, str(xlsx_path), target_id=target_id)

    csv_df = pd.read_csv(csv_path, dtype=str)
    xlsx_df = pd.read_excel(xlsx_path, dtype=str)

    assert csv_df.fillna("").values.tolist() == xlsx_df.fillna("").values.tolist()


def test_export_empty_history_writes_header_only_ac3(tmp_path):
    conn = store.connect(":memory:")
    target_id = store.add_target(
        conn,
        Target(
            name="Boş Hedef",
            url="http://example.test/empty",
            name_selector=".t",
            price_selector=".p",
            default_currency="TRY",
        ),
    )
    out = tmp_path / "empty.csv"

    export.export_csv(conn, str(out), target_id=target_id)

    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    assert rows == [export.COLUMNS]


def test_export_all_targets_includes_every_target_ac4(tmp_path):
    conn, target_id_1 = _seeded_conn()
    target_id_2 = store.add_target(
        conn,
        Target(
            name="Başka Ürün",
            url="http://example.test/other",
            name_selector=".t",
            price_selector=".p",
            default_currency="TRY",
        ),
    )
    store.save_snapshot(
        conn,
        PriceSnapshot(
            target_id=target_id_2,
            timestamp=datetime(2026, 8, 10, tzinfo=timezone.utc),
            raw_price="50 TL",
            price=Decimal("50"),
            currency="TRY",
            in_stock=None,
        ),
    )
    out = tmp_path / "all.csv"

    export.export_csv(conn, str(out))

    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    names = {row["hedef_adi"] for row in rows}
    assert len(rows) == 3
    assert names == {"Kulaklık X200", "Başka Ürün"}


def test_export_overwrites_existing_file_ac5(tmp_path):
    conn, target_id = _seeded_conn()
    out = tmp_path / "history.csv"
    out.write_text("stale content that should be replaced\n", encoding="utf-8")

    export.export_csv(conn, str(out), target_id=target_id)

    with open(out, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert "stale content" not in out.read_text(encoding="utf-8")
