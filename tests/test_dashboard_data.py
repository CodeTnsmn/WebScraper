from datetime import datetime, timezone
from decimal import Decimal

from dashboard.data import build_chart_dataframe, latest_snapshot
from webscraper.models import PriceSnapshot


def _snap(price, ts, target_id=1):
    return PriceSnapshot(
        target_id=target_id,
        timestamp=ts,
        raw_price=f"{price}",
        price=Decimal(str(price)) if price is not None else None,
        currency="TRY",
        in_stock=True,
    )


def test_build_chart_dataframe_point_count_matches_history_ac2():
    history = [
        _snap(100, datetime(2026, 8, 1, tzinfo=timezone.utc)),
        _snap(110, datetime(2026, 8, 2, tzinfo=timezone.utc)),
        _snap(105, datetime(2026, 8, 3, tzinfo=timezone.utc)),
    ]

    df = build_chart_dataframe({"Site A": history})

    assert len(df) == 3
    assert list(df.columns) == ["Site A"]


def test_build_chart_dataframe_series_count_matches_selected_targets_ac3():
    history_a = [_snap(100, datetime(2026, 8, 1, tzinfo=timezone.utc))]
    history_b = [
        _snap(90, datetime(2026, 8, 1, tzinfo=timezone.utc)),
        _snap(95, datetime(2026, 8, 2, tzinfo=timezone.utc)),
    ]

    df = build_chart_dataframe({"Site A": history_a, "Site B": history_b})

    assert set(df.columns) == {"Site A", "Site B"}


def test_build_chart_dataframe_skips_snapshots_without_numeric_price():
    history = [_snap(None, datetime(2026, 8, 1, tzinfo=timezone.utc))]

    df = build_chart_dataframe({"Site A": history})

    assert df.empty


def test_latest_snapshot_returns_most_recent_by_timestamp_ac4():
    older = _snap(100, datetime(2026, 8, 1, tzinfo=timezone.utc))
    newer = _snap(120, datetime(2026, 8, 15, tzinfo=timezone.utc))

    result = latest_snapshot([older, newer])

    assert result is newer
    assert result.price == Decimal("120")


def test_latest_snapshot_empty_history_returns_none():
    assert latest_snapshot([]) is None
