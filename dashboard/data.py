"""Pure, Streamlit-independent helpers for the dashboard (unit-testable in isolation).

Deliberately does not import webscraper.fetch/collect/sites — only shapes data that
was already read from webscraper.store (see docs/architecture.md dashboard boundary).
"""

import pandas as pd

from webscraper.models import PriceSnapshot


def build_chart_dataframe(histories: dict[str, list[PriceSnapshot]]) -> pd.DataFrame:
    """One column per target label, indexed by timestamp, values are float price.

    Snapshots without a numeric price are skipped (nothing to plot).
    """
    rows = [
        {"Hedef": label, "Zaman": snapshot.timestamp, "Fiyat": float(snapshot.price)}
        for label, history in histories.items()
        for snapshot in history
        if snapshot.price is not None
    ]
    if not rows:
        return pd.DataFrame(columns=list(histories.keys()))
    df = pd.DataFrame(rows)
    return df.pivot_table(index="Zaman", columns="Hedef", values="Fiyat")


def latest_snapshot(history: list[PriceSnapshot]) -> PriceSnapshot | None:
    """Snapshot with the largest timestamp, or None if history is empty."""
    if not history:
        return None
    return max(history, key=lambda snapshot: snapshot.timestamp)
