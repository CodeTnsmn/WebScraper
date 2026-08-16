from datetime import datetime, timezone
from decimal import Decimal

from webscraper import store
from webscraper.models import PriceSnapshot, Target


def _make_target(**overrides):
    defaults = dict(
        name="Kulaklık X200",
        url="http://example.test/product",
        name_selector=".product-title",
        price_selector=".product-price",
        default_currency="TRY",
    )
    defaults.update(overrides)
    return Target(**defaults)


def test_add_and_list_target_roundtrip_ac1():
    conn = store.connect(":memory:")

    target_id = store.add_target(conn, _make_target())
    targets = store.list_targets(conn)

    assert len(targets) == 1
    assert targets[0].id == target_id
    assert targets[0].name == "Kulaklık X200"
    assert targets[0].default_currency == "TRY"


def test_get_history_returns_snapshots_oldest_first_ac4():
    conn = store.connect(":memory:")
    target_id = store.add_target(conn, _make_target())

    older = PriceSnapshot(
        target_id=target_id,
        timestamp=datetime(2026, 8, 1, tzinfo=timezone.utc),
        raw_price="1.199,00 TL",
        currency="TRY",
        in_stock=True,
        price=Decimal("1199.00"),
    )
    newer = PriceSnapshot(
        target_id=target_id,
        timestamp=datetime(2026, 8, 15, tzinfo=timezone.utc),
        raw_price="1.299,90 TL",
        currency="TRY",
        in_stock=True,
        price=Decimal("1299.90"),
    )
    store.save_snapshot(conn, newer)
    store.save_snapshot(conn, older)

    history = store.get_history(conn, target_id)

    assert [s.price for s in history] == [Decimal("1199.00"), Decimal("1299.90")]


def test_delete_target_keeps_existing_snapshots_ac5():
    conn = store.connect(":memory:")
    target_id = store.add_target(conn, _make_target())
    store.save_snapshot(
        conn,
        PriceSnapshot(
            target_id=target_id,
            timestamp=datetime.now(timezone.utc),
            raw_price="10 TL",
            currency="TRY",
            in_stock=None,
        ),
    )

    store.delete_target(conn, target_id)

    assert store.list_targets(conn) == []
    assert len(store.get_history(conn, target_id)) == 1
