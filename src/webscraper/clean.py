import re
from decimal import Decimal, InvalidOperation

from webscraper.exceptions import CleanError

_ALLOWED_CHARS = re.compile(r"[^\d,.\-]")


def clean_price(raw_price: str) -> Decimal:
    """Normalizes a raw price string (TR or US thousands/decimal style) to Decimal.

    Currency symbols/codes and whitespace are stripped. When both '.' and ',' are
    present, whichever appears last is treated as the decimal separator. When only
    one separator type is present, a single occurrence with 1-2 trailing digits is
    treated as decimal (e.g. cents); otherwise it's treated as a thousands separator.
    """
    numeric = _ALLOWED_CHARS.sub("", raw_price.strip())
    if not numeric or not any(ch.isdigit() for ch in numeric):
        raise CleanError(f"could not parse a price from {raw_price!r}")

    has_dot = "." in numeric
    has_comma = "," in numeric

    if has_dot and has_comma:
        if numeric.rfind(",") > numeric.rfind("."):
            normalized = numeric.replace(".", "").replace(",", ".")
        else:
            normalized = numeric.replace(",", "")
    elif has_comma:
        last = numeric.rfind(",")
        frac_len = len(numeric) - last - 1
        normalized = numeric.replace(",", ".") if numeric.count(",") == 1 and frac_len in (1, 2) else numeric.replace(",", "")
    elif has_dot:
        last = numeric.rfind(".")
        frac_len = len(numeric) - last - 1
        normalized = numeric if numeric.count(".") == 1 and frac_len in (1, 2) else numeric.replace(".", "")
    else:
        normalized = numeric

    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise CleanError(f"could not parse a price from {raw_price!r}") from exc
