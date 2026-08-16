import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone

import requests

from webscraper import config, store
from webscraper.exceptions import WebScraperError
from webscraper.fetch import fetch_html
from webscraper.models import PriceSnapshot, Target
from webscraper.sites.generic import GenericSelectorAdapter, SelectorConfig


@dataclass
class CollectResult:
    target_id: int
    status: str  # "ok" or "failed"
    error: str | None = None


def _adapter_for(target: Target) -> GenericSelectorAdapter:
    return GenericSelectorAdapter(
        SelectorConfig(
            name_selector=target.name_selector,
            price_selector=target.price_selector,
            default_currency=target.default_currency,
            stock_selector=target.stock_selector,
            stock_in_stock_text=target.stock_in_stock_text,
        )
    )


def collect_target(
    conn: sqlite3.Connection, target: Target, *, session: requests.Session | None = None
) -> CollectResult:
    """Fetches+parses one target and stores a snapshot. No snapshot is written on failure."""
    try:
        html = fetch_html(target.url, session=session)
        parsed = _adapter_for(target).parse(html)
    except WebScraperError as exc:
        return CollectResult(target_id=target.id, status="failed", error=str(exc))

    snapshot = PriceSnapshot(
        target_id=target.id,
        timestamp=datetime.now(timezone.utc),
        raw_price=parsed.raw_price,
        currency=parsed.currency,
        in_stock=parsed.in_stock,
    )
    store.save_snapshot(conn, snapshot)
    return CollectResult(target_id=target.id, status="ok")


def collect_all(
    conn: sqlite3.Connection,
    targets: list[Target],
    *,
    session: requests.Session | None = None,
    sleep_fn=time.sleep,
) -> list[CollectResult]:
    """Sequentially collects every target; one failure does not stop the rest (AC-3)."""
    results = []
    for index, target in enumerate(targets):
        results.append(collect_target(conn, target, session=session))
        if index < len(targets) - 1:
            sleep_fn(config.RATE_LIMIT_DELAY_SECONDS)
    return results
