from dataclasses import dataclass

from bs4 import BeautifulSoup

from webscraper.exceptions import ParseError
from webscraper.sites.base import ParsedProduct, SiteAdapter


@dataclass
class SelectorConfig:
    """CSS selectors describing where to find product data on a page.

    Adding support for a new site means writing a new SelectorConfig, not new code
    (Open/Closed — see docs/architecture.md).
    """

    name_selector: str
    price_selector: str
    default_currency: str
    stock_selector: str | None = None
    stock_in_stock_text: str | None = None


class GenericSelectorAdapter(SiteAdapter):
    def __init__(self, selectors: SelectorConfig):
        self._selectors = selectors

    def parse(self, html: str) -> ParsedProduct:
        soup = BeautifulSoup(html, "lxml")

        name_el = soup.select_one(self._selectors.name_selector)
        if name_el is None:
            raise ParseError(f"name selector not found: {self._selectors.name_selector!r}")

        price_el = soup.select_one(self._selectors.price_selector)
        if price_el is None:
            raise ParseError(f"price selector not found: {self._selectors.price_selector!r}")

        in_stock: bool | None = None
        if self._selectors.stock_selector is not None:
            stock_el = soup.select_one(self._selectors.stock_selector)
            if stock_el is not None:
                stock_text = stock_el.get_text(strip=True)
                in_stock = stock_text == self._selectors.stock_in_stock_text

        return ParsedProduct(
            name=name_el.get_text(strip=True),
            raw_price=price_el.get_text(strip=True),
            currency=self._selectors.default_currency,
            in_stock=in_stock,
        )
