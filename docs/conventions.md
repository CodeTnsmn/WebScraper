# Kodlama Konvansiyonları

## Stack
- Python 3.11+
- HTTP: `requests` (statik HTML) + `playwright` (JS-render gerektiren siteler, opsiyonel)
- Parse: `beautifulsoup4` + `lxml`
- Veri: `pandas` (temizleme/export), `SQLite` (depolama, stdlib `sqlite3`)
- Zamanlama: `APScheduler`
- Panel: `streamlit`
- Test: `pytest`

## Adlandırma
- Modül/dosya: `snake_case`. Sınıf: `PascalCase`. Fonksiyon/değişken: `snake_case`.
- Site adaptörleri: `webscraper/sites/<site_adi>.py`, sınıf adı `<SiteAdi>Adapter`.

## Hata Yönetimi
- Ağ hataları (`requests.RequestException`) yakalanır, retry uygulanır (max 3, exponential backoff).
- Parse hatası (beklenen selector bulunamadı) sessizce yutulmaz — loglanır, o hedef
  `failed` olarak işaretlenir, diğer hedefler etkilenmez.
- Genel `except Exception` yasak; spesifik exception tipleri yakalanır.

## Diğer
- Tüm fiyat alanları `Decimal`.
- Zaman damgaları UTC, ISO-8601.
- Sabit değerler (rate-limit süresi, retry sayısı vb.) `config.py`'de merkezi tutulur.
