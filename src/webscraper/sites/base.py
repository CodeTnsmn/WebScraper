from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ParsedProduct:
    name: str
    raw_price: str
    currency: str
    in_stock: bool | None


class SiteAdapter(ABC):
    """Extracts product data from a downloaded HTML page.

    Implementations must not perform HTTP requests or disk I/O — they only parse
    the HTML string they are given (see docs/architecture.md).
    """

    @abstractmethod
    def parse(self, html: str) -> ParsedProduct: ...
