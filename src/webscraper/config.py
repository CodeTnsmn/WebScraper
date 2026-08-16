"""Centralized constants (Golden Rule 7 — no magic numbers scattered in code)."""

REQUEST_TIMEOUT_SECONDS = 10
MAX_RETRIES = 3
RETRY_BACKOFF_BASE_SECONDS = 1.0
DEFAULT_USER_AGENT = "WebScraper/0.1 (+https://github.com/CodeTnsmn/WebScraper)"

DEFAULT_DB_PATH = "webscraper.db"
DEFAULT_EXPORT_DIR = "output"

RATE_LIMIT_DELAY_SECONDS = 2.0
