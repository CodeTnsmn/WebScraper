from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from streamlit.testing.v1 import AppTest

from webscraper import store
from webscraper.models import PriceSnapshot, Target

APP_PATH = str(Path(__file__).resolve().parent.parent / "dashboard" / "app.py")


def test_empty_database_shows_info_message_no_crash_ac1(tmp_path, monkeypatch):
    db_path = str(tmp_path / "empty.db")
    store.connect(db_path)  # create schema, no targets
    monkeypatch.setenv("WEBSCRAPER_DB", db_path)

    at = AppTest.from_file(APP_PATH).run()

    assert not at.exception
    assert any("henüz takip edilen hedef yok" in info.value.lower() for info in at.info)


def test_target_with_history_renders_chart_and_metrics_ac4(tmp_path, monkeypatch):
    db_path = str(tmp_path / "seeded.db")
    conn = store.connect(db_path)
    target_id = store.add_target(
        conn,
        Target(
            name="Kulaklık X200",
            url="http://example.test/product",
            name_selector=".n",
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
            in_stock=True,
        ),
    )
    monkeypatch.setenv("WEBSCRAPER_DB", db_path)

    at = AppTest.from_file(APP_PATH).run()

    assert not at.exception
    assert len(at.metric) == 2
    assert "1299.90" in at.metric[0].value
