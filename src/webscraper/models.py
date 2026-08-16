from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Target:
    name: str
    url: str
    name_selector: str
    price_selector: str
    default_currency: str
    stock_selector: str | None = None
    stock_in_stock_text: str | None = None
    id: int | None = None


@dataclass
class PriceSnapshot:
    target_id: int
    timestamp: datetime
    raw_price: str
    currency: str
    in_stock: bool | None
    price: Decimal | None = None
    id: int | None = None
