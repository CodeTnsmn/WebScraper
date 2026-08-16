# Mimari

## Genel Bakış
CLI + kütüphane çekirdek, üstünde opsiyonel Streamlit paneli. Bkz. `docs/decisions/0001-app-format.md`.

## Modüller
| Modül | Sorumluluk | Yasaklar |
|---|---|---|
| `webscraper.fetch` | HTTP istekleri, retry, rate-limit, user-agent rotasyonu | Parsing yapamaz |
| `webscraper.parse` | Site-özel HTML→veri çıkarma (selector bazlı) | HTTP isteği atamaz, disk yazamaz |
| `webscraper.clean` | Ham veriyi normalize eder (fiyat/para birimi/whitespace) | Kaynak siteye bağımlı olamaz |
| `webscraper.store` | SQLite'a yazma/okuma, geçmiş fiyat serisi | Parsing/export mantığı içeremez |
| `webscraper.export` | CSV/Excel'e aktarma | DB şemasına doğrudan erişemez, `store` üzerinden okur |
| `webscraper.schedule` | APScheduler ile periyodik çalıştırma | Parsing/export mantığı içeremez |
| `webscraper.cli` | Komut satırı giriş noktası | İş mantığı içermez, sadece orkestrasyon |
| `dashboard/` (Streamlit) | Fiyat trendi + rakip karşılaştırma görselleştirme | `store` dışında veri kaynağına erişemez, scraping tetikleyemez |

## Veri akışı
`fetch` → `parse` → `clean` → `store` (SQLite) → `export` (CSV/Excel) ve/veya `dashboard` (okuma-only).

## Site adaptörleri
Her hedef site için `webscraper/sites/<site_adi>.py` içinde `SiteAdapter` arayüzünü
uygulayan bir sınıf. Yeni site eklemek var olan adaptörleri değiştirmez (Open/Closed).

## Sınırlar
- `dashboard/` asla `fetch`/`parse` çağırmaz — sadece `store`'dan okur.
- Site adaptörleri birbirinin internal detayına erişemez.
- Scraping hedefi sitenin `robots.txt`'i ve kullanım şartları ihlal edilmez (bkz. domain.md).
