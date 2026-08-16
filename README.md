# WebScraper

E-ticaret fiyat takibi ve rakip analizi için web scraper.

## Özellikler
- Hedef web sitelerinden ürün fiyat/stok verisi çıkarma (site adaptörleri)
- Otomatik, zamanlanmış veri toplama
- Veri temizleme ve normalize etme (fiyat, para birimi)
- CSV / Excel / SQLite'a aktarma
- Opsiyonel Streamlit paneli: fiyat trendi ve rakip karşılaştırması

## Mimari
CLI + kütüphane çekirdek, üstünde opsiyonel görselleştirme paneli. Detay: [docs/architecture.md](docs/architecture.md), karar gerekçesi: [docs/decisions/0001-app-format.md](docs/decisions/0001-app-format.md).

## Geliştirme disiplini
Bu proje spec-first bir döngüyle geliştirilir (INTENT → SPEC → PLAN → BUILD → REVIEW → VERIFY).
Süreç ve rol tanımları yerel `AGENTS.md` dosyasında tutulur (repoya dahil değildir).

## Kurulum
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Kullanım
```bash
python -m webscraper.cli --help
```

## Panel (opsiyonel)
Fiyat trendi ve rakip karşılaştırma görselleştirmesi:
```bash
streamlit run dashboard/app.py
```
Farklı bir veritabanı dosyası kullanmak için `WEBSCRAPER_DB` ortam değişkenini ayarlayın.

## Durum
Proje iskelet aşamasında. Spec'ler `specs/` altında ilerledikçe eklenecek.
