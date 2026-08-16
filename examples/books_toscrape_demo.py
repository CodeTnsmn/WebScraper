"""Canlı örnek — gerçek bir siteye karşı uçtan uca çalışır (Spec 0008).

Hedef: books.toscrape.com — scraping pratiği için hazırlanmış, herkese açık, ToS/
robots.txt riski taşımayan bir demo mağaza. Gerçek ağ isteği attığı için pytest
suite'inin bir parçası DEĞİLDİR (bkz. docs/testing.md). Elle çalıştırılır:

    python examples/books_toscrape_demo.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from webscraper import store  # noqa: E402
from webscraper.collect import collect_all  # noqa: E402
from webscraper.export import export_csv  # noqa: E402
from webscraper.models import Target  # noqa: E402

DB_PATH = str(Path(__file__).resolve().parent / "books_toscrape_demo.db")
CSV_PATH = str(Path(__file__).resolve().parent / "books_toscrape_demo.csv")

TARGETS = [
    Target(
        name="A Light in the Attic (books.toscrape.com)",
        url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        name_selector=".product_main h1",
        price_selector=".product_main .price_color",
        default_currency="GBP",
        stock_selector=".product_main .instock.availability",
        stock_in_stock_text="In stock (22 available)",
    ),
    Target(
        name="Soumission (books.toscrape.com)",
        url="https://books.toscrape.com/catalogue/soumission_998/index.html",
        name_selector=".product_main h1",
        price_selector=".product_main .price_color",
        default_currency="GBP",
        stock_selector=".product_main .instock.availability",
        stock_in_stock_text="In stock (20 available)",
    ),
]


def main() -> None:
    conn = store.connect(DB_PATH)

    existing_urls = {target.url for target in store.list_targets(conn)}
    for target in TARGETS:
        if target.url not in existing_urls:
            store.add_target(conn, target)

    targets = store.list_targets(conn)
    print(f"{len(targets)} hedef için gerçek ağ isteğiyle toplama başlıyor...")
    for result in collect_all(conn, targets):
        print(f"  hedef={result.target_id} durum={result.status} hata={result.error or '-'}")

    export_csv(conn, CSV_PATH)
    print(f"Dışa aktarıldı: {CSV_PATH}")


if __name__ == "__main__":
    main()
