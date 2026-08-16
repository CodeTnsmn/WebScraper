import time

import requests

from webscraper import config
from webscraper.exceptions import FetchError


def fetch_html(url: str, *, session: requests.Session | None = None) -> str:
    """Download a page's HTML, retrying transient network errors with backoff.

    Non-2xx HTTP responses are treated as permanent failures and are not retried.
    """
    http = session or requests.Session()
    headers = {"User-Agent": config.DEFAULT_USER_AGENT}

    last_error: Exception | None = None
    for attempt in range(config.MAX_RETRIES):
        try:
            response = http.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT_SECONDS)
        except requests.RequestException as exc:
            last_error = exc
            if attempt < config.MAX_RETRIES - 1:
                time.sleep(config.RETRY_BACKOFF_BASE_SECONDS * (2**attempt))
            continue

        if response.status_code != 200:
            raise FetchError(f"{url} returned HTTP {response.status_code}")
        if "charset" not in response.headers.get("Content-Type", "").lower():
            # No declared charset: requests falls back to ISO-8859-1 per RFC 2616,
            # which mangles non-ASCII (e.g. "£" -> "Â£") on pages that are actually
            # UTF-8 but don't say so. Sniff instead when the server didn't declare it.
            response.encoding = response.apparent_encoding
        return response.text

    raise FetchError(f"Failed to fetch {url} after {config.MAX_RETRIES} attempts: {last_error}")
