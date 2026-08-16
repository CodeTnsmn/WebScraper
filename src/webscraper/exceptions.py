class WebScraperError(Exception):
    """Base class for all webscraper errors."""


class FetchError(WebScraperError):
    """Raised when a page could not be downloaded (network or non-2xx status)."""


class ParseError(WebScraperError):
    """Raised when required data could not be extracted from downloaded HTML."""


class CleanError(WebScraperError):
    """Raised when a raw price string cannot be normalized to a Decimal."""
