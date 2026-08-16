# Spec 0003 — Veri Temizleme

## Intent
Sitelerden çıkarılan ham fiyat metni ("1.299,90 TL", "$19.99", "1,299.00" gibi) site
formatına göre farklı yazılır; bu ham metin doğrudan karşılaştırılamaz/toplanamaz.
Kullanıcının rakip analizi yapabilmesi için tüm fiyatlar tutarlı, tek bir sayısal
biçime (Decimal) normalize edilmeli. Bilerek yapılmayacak: döviz kuru çevrimi (TL↔USD
gibi) — bu spec yalnızca metni sayıya çevirir, para birimini değiştirmez.

## Requirements
- Ham fiyat metni, binlik/ondalık ayıracı TR biçiminde (nokta=binlik, virgül=ondalık)
  veya US biçiminde (virgül=binlik, nokta=ondalık) olsa da doğru sayısal değere
  çevrilebilmeli.
- Para birimi sembolü/kodu (TL, ₺, $, USD, €, vb.) ve boşluklar temizlenirken sayısal
  değeri etkilememeli.
- Toplama akışı (Spec 0002), çıkarılan ham fiyatı otomatik olarak temizleyip snapshot'a
  sayısal değer olarak da kaydetmeli — böylece geçmiş sorgularken hem ham metin hem
  sayısal değer erişilebilir olur.
- Fiyat metni sayıya çevrilemeyecek kadar bozuksa (beklenmeyen biçim), bu durum açıkça
  bir hata olarak ayırt edilebilmeli ve o hedefin toplaması "başarısız" sayılmalı
  (Spec 0002 AC-3 ile aynı davranış — snapshot kısmi/yanlış veriyle kaydedilmez).

## Constraints
- Fiyat her zaman `Decimal` olarak tutulur, `float` kullanılmaz (yuvarlama hatası
  riski — bkz. docs/domain.md).
- **Kapsam dışı (bilinçli):** döviz çevrimi, negatif/indirim yüzdesi ayrıştırma.

## Context
Bkz. `docs/domain.md` (Decimal kuralı), Spec 0001 (ham fiyat çıkarımı), Spec 0002
(snapshot kaydı — `PriceSnapshot.price` alanı bu spec'le doldurulur).

## Acceptance Criteria
- AC-1: "1.299,90 TL" → `Decimal("1299.90")` (TR biçimi: nokta binlik, virgül ondalık).
- AC-2: "$19.99" → `Decimal("19.99")` (US biçimi: nokta ondalık, sembol yok sayılır).
- AC-3: "1,299.00" → `Decimal("1299.00")` (US biçimi: virgül binlik).
- AC-4: Baştaki/sondaki boşluklar ve para birimi kodu/sembolü (TL, ₺, $, USD, €) temizlenip
  yalnızca sayı kalır; sonuç yukarıdaki gibi doğru olur.
- AC-5: Sayı içermeyen veya tanınmayan bir biçimdeki metin (ör. "Fiyat için tıklayın")
  verildiğinde `CleanError` fırlatılır.
- AC-6: Spec 0002'deki "tümünü topla" akışı çalıştığında, başarılı her snapshot'ta
  `price` alanı ham metinden doğru hesaplanmış `Decimal` değerini içerir; temizleme
  başarısız olursa o hedef için snapshot kaydedilmez (Spec 0002 AC-3 ile tutarlı).

## Verification Evidence
- AC-1↔`test_tr_format_dot_thousands_comma_decimal_ac1`, AC-2↔`test_us_format_dot_decimal_ac2`, AC-3↔`test_us_format_comma_thousands_dot_decimal_ac3`, AC-4↔`test_currency_symbols_and_whitespace_stripped_ac4` (5 parametre), AC-5↔`test_unparseable_text_raises_clean_error_ac5`, AC-6↔`test_collect_target_saves_snapshot_on_success_ac2` (price alanı kontrolü)+`test_collect_target_no_snapshot_on_clean_failure_ac6`.
- Sonuç: 25/25 test yeşil (tüm paket, `pytest tests/`).
- Mutasyon muhakemesi: `clean.py`'de TR/US ayırt eden `rfind(",") > rfind(".")` koşulu ters çevrilse AC-1 ve AC-3 birbirini geçersiz kılar (biri kırmızı olur); `collect.py`'de `clean_price` çağrısı try bloğu dışına alınsa AC-6 testi kırmızı olur (CleanError yakalanmaz, "failed" yerine exception fırlar).

## Definition of Done
- [x] Tüm AC'ler karşılandı ve teste bağlandı
- [x] Bağımsız REVIEW geçti (aynı oturumda QA şapkasıyla)
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
