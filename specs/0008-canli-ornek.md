# Spec 0008 — Canlı Örnek (Gerçek Siteye Karşı Uçtan Uca)

## Intent
Şu ana kadarki tüm testler (Spec 0001-0007) fixture/mock HTML ile çalışıyor — sistemin
gerçek bir siteye karşı gerçekten çalıştığı hiç kanıtlanmadı. Kullanıcı bunu gözle
görebilmeli: gerçek bir HTTP isteği, gerçek bir parse, gerçek bir export. Hedef site
olarak **books.toscrape.com** seçildi — scraping pratiği için özel olarak hazırlanmış,
herkese açık, robots.txt kısıtlaması olmayan, ToS/hukuki risk taşımayan bir demo mağaza
(gerçek bir e-ticaret sitesi hedeflemek burada bilerek yapılmıyor). Bilerek
yapılmayacak: bu betiğin pytest suite'ine dahil edilmesi (docs/testing.md: canlı ağ
isteği testte yasak) — bağımsız, elle çalıştırılan bir örnek olarak kalır.

## Requirements
- `examples/` altında, iki gerçek books.toscrape.com ürününü hedef olarak tanımlayan,
  çalıştırıldığında gerçek ağ isteği atıp veriyi toplayan ve CSV'ye aktaran bağımsız
  bir betik olmalı.
- Betik var olan `webscraper` kütüphanesini (store/collect/export) olduğu gibi
  kullanmalı — örnek için özel/paralel bir kod yolu yazılmamalı.
- Betik tekrar çalıştırıldığında aynı hedefleri yinelemeden (idempotent) kullanmalı.
- README'de bu örneğin nasıl çalıştırılacağı ve neden pytest'e dahil olmadığı
  açıklanmalı.

## Constraints
- **Kapsam dışı (bilinçli):** CI'da otomatik çalıştırma (dış ağa bağımlı olduğu için
  flaky olur — AP-03 riski), gerçek bir e-ticaret sitesi hedefleme.

## Context
Selector'lar gerçek sayfa üzerinde elle doğrulandı (bkz. Verification Evidence).
Kullanılan modüller: Spec 0001 (fetch/parse), 0002 (store/collect), 0004 (export).

## Acceptance Criteria
- AC-1: Betik ilk çalıştırıldığında, iki hedef veritabanına eklenir ve her ikisi için
  de gerçek ağ isteğiyle başarılı (`status=ok`) bir snapshot oluşur.
- AC-2: Betik ikinci kez çalıştırıldığında, hedef sayısı ikide kalır (tekrar
  eklenmez) — yeni bir snapshot turu yine de eklenir.
- AC-3: Çalıştırma sonunda oluşan CSV dosyasında her iki hedefin de en az bir satırı,
  doğru şekilde temizlenmiş (Decimal'e çevrilmiş) sayısal fiyatla birlikte bulunur.

## Verification Evidence
- Selector'lar `https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html`
  ve `.../soumission_998/index.html` sayfalarına gerçek `requests` isteğiyle elle
  doğrulandı: `.product_main h1` (ad), `.product_main .price_color` (fiyat, "£51.77"
  / "£50.10"), `.product_main .instock.availability` (stok metni, tam eşleşme).
- **AC-1 (ilk çalıştırma):** `python examples/books_toscrape_demo.py` çalıştırıldı,
  2 hedef eklendi, ikisi de `durum=ok`.
- **AC-2 (idempotency):** betik ikinci kez çalıştırıldı; `store.list_targets` hâlâ
  2 hedef döndü (tekrar eklenmedi), her hedefin snapshot sayısı 1→2'ye çıktı (yeni
  tur eklendi, hedef değil).
- **AC-3 (export doğruluğu):** çıkan CSV'de her iki hedef için de doğru `Decimal`
  fiyat (51.77 / 50.10) ve `GBP` para birimi bulundu.
- **Yan bulgu (AP-01, bkz. Spec 0001 Revizyon Notları):** ilk çalıştırmada ham fiyat
  sütununda "Â£51.77" (mojibake) görüldü — `fetch.py`'deki charset-sniffing eksikliği
  yüzünden. `fetch.py` düzeltildikten sonra betik tekrar çalıştırıldı, CSV'de doğru
  "£51.77" / "£50.10" görüldü; bu spec'in kendisi bu gerçek hatayı yakalamış oldu
  (fixture/mock testlerin kaçırdığı bir sınıf hata — canlı örneğin asıl gerekçesi).

## Definition of Done
- [x] Tüm AC'ler karşılandı (manuel doğrulama — canlı ağ testi pytest'e girmediği için
      otomatik teste bağlanmadı, bkz. Constraints)
- [x] Bağımsız REVIEW geçti (aynı oturumda QA şapkasıyla)
- [x] Test anlamı doğrulandı (mutasyon — n/a, otomatik test yok)
- [x] Docs/ADR gerekiyorsa güncellendi (README'ye eklendi)

### Scorecard
| Metrik | Değer |
|---|---|
| Spec revizyon sayısı | 0 |
| Düzeltme turu sayısı | 0 |
| Bulgu gerçek/gürültü oranı | - |
| Regresyon sayısı | 0 |
| Kaçan hata (sonradan bulunan) | 0 |

## Revizyon Notları
Yok.
