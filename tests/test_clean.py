from decimal import Decimal

import pytest

from webscraper.clean import clean_price
from webscraper.exceptions import CleanError


def test_tr_format_dot_thousands_comma_decimal_ac1():
    assert clean_price("1.299,90 TL") == Decimal("1299.90")


def test_us_format_dot_decimal_ac2():
    assert clean_price("$19.99") == Decimal("19.99")


def test_us_format_comma_thousands_dot_decimal_ac3():
    assert clean_price("1,299.00") == Decimal("1299.00")


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("  1.299,90 TL  ", Decimal("1299.90")),
        ("₺1.299,90", Decimal("1299.90")),
        ("1299 TL", Decimal("1299")),
        ("USD 19.99", Decimal("19.99")),
        ("€1.234", Decimal("1234")),
    ],
)
def test_currency_symbols_and_whitespace_stripped_ac4(raw, expected):
    assert clean_price(raw) == expected


def test_unparseable_text_raises_clean_error_ac5():
    with pytest.raises(CleanError):
        clean_price("Fiyat için tıklayın")
