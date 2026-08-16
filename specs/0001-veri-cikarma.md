# Spec 0001 — Hedef Web Sitelerinden Veri Çıkarma

## Intent
Kullanıcı takip ettiği bir ürünün URL'ini verdiğinde sistem o sayfadan ürün adı, fiyat,
para birimi ve stok durumunu çıkarabilmeli. Farklı e-ticaret siteleri farklı HTML
yapısına sahip olduğundan, çıkarma mantığı siteye özel değil, **CSS selector ile
yapılandırılabilir** olmalı — böylece yeni bir site eklemek kod değişikliği değil,
konfigürasyon eklemek anlamına gelir. Bilerek yapılmayacak: JavaScript ile render edilen
siteler (bu spec kapsamında yalnızca statik HTML), login gerektiren sayfalar.

## Requirements
- Bir hedef URL'den HTML indirilebilmeli.
- İndirilen HTML'den, verilen selector kurallarına göre şu alanlar çıkarılabilmeli:
  ürün adı, ham fiyat metni, para birimi (varsa selector'dan, yoksa varsayılan),
  stok durumu (varsa selector'dan, yoksa bilinmiyor/None).
- Sayfa indirilemezse (ağ hatası) veya beklenen alan HTML'de bulunamazsa, hata açıkça
  ayırt edilebilmeli (ağ hatası ≠ parse hatası).
- Geçici ağ hatalarında otomatik yeniden deneme yapılmalı.

## Constraints
- Ağ isteklerinde makul bir zaman aşımı ve deneme sınırı olmalı (kaynak siteye
  aşırı yük bindirilmemeli).
- **Kapsam dışı (bilinçli):** JS-render gerektiren siteler (Playwright entegrasyonu
  ileride ayrı bir spec'te), login/oturum gerektiren sayfalar, robots.txt otomatik
  kontrolü (bu spec'te elle uyulması dokümante edilir, otomatik engelleme yazılmaz —
  ayrı bir spec'e bırakılır).

## Context
Bkz. `docs/architecture.md` — `fetch` ve `parse`/site-adaptör modülleri. ADR 0001
(CLI+kütüphane çekirdek).

## Acceptance Criteria
- AC-1: Geçerli bir HTML sayfası ve doğru selector'lar verildiğinde ürün adı ve ham
  fiyat metni doğru çıkarılır.
- AC-2: Selector'da tanımlı stok elemanı sayfada yoksa stok durumu `None` (bilinmiyor)
  döner, hata fırlatmaz.
- AC-3: Fiyat elemanı HTML'de hiç bulunamazsa `ParseError` fırlatılır ve hata mesajında
  hangi selector'ın başarısız olduğu belirtilir.
- AC-4: Ağ isteği zaman aşımına uğrarsa veya bağlantı hatası verirse, en fazla 3 deneme
  yapılır (exponential backoff ile); tüm denemeler başarısız olursa `FetchError`
  fırlatılır.
- AC-5: HTTP 200 dışı bir durum kodu (ör. 404, 500) `FetchError` fırlatır, retry
  denenmeden (kalıcı hata, retry anlamsız) — yalnızca ağ/bağlantı seviyeli hatalar
  retry edilir.

## Verification Evidence
- AC-1↔`test_parse_extracts_name_and_price_ac1`, AC-2↔`test_parse_missing_stock_element_returns_none_ac2`+`test_parse_in_stock_text_match_ac2`, AC-3↔`test_parse_missing_price_raises_parse_error_ac3`+`test_parse_missing_name_raises_parse_error_ac3`, AC-4↔`test_fetch_html_retries_on_connection_error_then_succeeds_ac4`+`test_fetch_html_all_retries_fail_raises_fetch_error_ac4`, AC-5↔`test_fetch_html_non_200_raises_fetch_error_without_retry_ac5`.
- Sonuç: 9/9 test yeşil (`pytest tests/test_fetch.py tests/test_sites_generic.py`).
- Mutasyon muhakemesi: `fetch.py`'de `status_code != 200` kontrolü kaldırılsa AC-5 testi kırmızı olur (call_count/exception kontrolü); `generic.py`'de `if name_el is None: raise` kaldırılsa AC-3 testi kırmızı olur (AttributeError yerine ParseError beklenir, farklı hata tipi testi kırar).

## Definition of Done
- [x] Tüm AC'ler karşılandı ve teste bağlandı
- [x] Bağımsız REVIEW geçti (aynı oturumda QA şapkasıyla yapıldı — bkz. not)
- [x] Test anlamı doğrulandı (mutasyon)
- [x] Docs/ADR gerekiyorsa güncellendi (gerekmedi)

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
