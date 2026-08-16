from pathlib import Path

import pytest

from webscraper.exceptions import ParseError
from webscraper.sites.generic import GenericSelectorAdapter, SelectorConfig

FIXTURES = Path(__file__).parent / "fixtures"

SELECTORS = SelectorConfig(
    name_selector=".product-title",
    price_selector=".product-price",
    default_currency="TRY",
    stock_selector=".stock-status",
    stock_in_stock_text="Stokta var",
)


def test_parse_extracts_name_and_price_ac1():
    html = (FIXTURES / "example_product.html").read_text(encoding="utf-8")
    result = GenericSelectorAdapter(SELECTORS).parse(html)

    assert result.name == "Kablosuz Kulaklık X200"
    assert result.raw_price == "1.299,90 TL"
    assert result.currency == "TRY"


def test_parse_missing_stock_element_returns_none_ac2():
    html = (FIXTURES / "example_product_no_stock.html").read_text(encoding="utf-8")
    result = GenericSelectorAdapter(SELECTORS).parse(html)

    assert result.in_stock is None


def test_parse_in_stock_text_match_ac2():
    html = (FIXTURES / "example_product.html").read_text(encoding="utf-8")
    result = GenericSelectorAdapter(SELECTORS).parse(html)

    assert result.in_stock is True


def test_parse_missing_price_raises_parse_error_ac3():
    html = (FIXTURES / "example_product_no_price.html").read_text(encoding="utf-8")

    with pytest.raises(ParseError, match=".product-price"):
        GenericSelectorAdapter(SELECTORS).parse(html)


def test_parse_missing_name_raises_parse_error_ac3():
    html = "<html><body><span class='product-price'>10 TL</span></body></html>"

    with pytest.raises(ParseError, match=".product-title"):
        GenericSelectorAdapter(SELECTORS).parse(html)
