# Spec 0002 — Otomatik Veri Toplama

## Intent
Kullanıcı tek tek URL çekmek yerine, takip ettiği tüm hedefleri (ürün+site) bir listede
tutup tek komutla hepsinin güncel fiyatını toplayabilmeli. Sonuç kalıcı olmalı ki geçmiş
fiyat serisi biriksin (rakip analizi ve trend için gerekli temel). Bir hedef başarısız
olursa diğerlerinin toplanması engellenmemeli. Bilerek yapılmayacak: paralel/eşzamanlı
istek atma (rate-limit riskini artırır, bu spec'te sıralı toplama yeterli).

## Requirements
- Hedefler (ürün adı, URL, site seçici konfigürasyonu, para birimi) kalıcı olarak
  eklenip listelenebilmeli.
- "Tümünü topla" komutu, tanımlı tüm hedefleri sırayla çeker, her biri için Spec
  0001'deki çıkarma akışını (fetch+parse) çalıştırır ve sonucu kalıcı depoya (fiyat
  geçmişi) bir "anlık görüntü" (snapshot) olarak kaydeder.
- Bir hedefin toplanması başarısız olursa (ağ/parse hatası) o hedef "başarısız" olarak
  işaretlenir/loglanır, toplama diğer hedeflerle devam eder — tek hata tüm çalıştırmayı
  durdurmaz.
- Bir hedefin geçmiş snapshot'ları zaman sırasıyla sorgulanabilmeli.
- Bir hedef silinse bile önceki snapshot'ları saklanmaya devam eder (domain.md kuralı).

## Constraints
- İstekler arası bekleme (rate-limit) uygulanır — art arda istekler arasında sabit bir
  gecikme olur.
- **Kapsam dışı (bilinçli):** paralel toplama, hedef URL doğrulama/robots.txt otomatik
  kontrolü (elle uyum sorumluluğu kullanıcıda, bkz. domain.md), veri temizleme (ham
  fiyat metni bu spec'te olduğu gibi saklanır — normalize etme Spec 0003'te).

## Context
Bkz. `docs/architecture.md` (`store`, `webscraper.cli` modülleri), Spec 0001 (fetch+parse).

## Acceptance Criteria
- AC-1: Yeni bir hedef eklendiğinde, hedef listesinde görünür ve alanları (ad, URL,
  para birimi) doğru saklanır.
- AC-2: "Tümünü topla" çalıştırıldığında, tanımlı N hedefin her biri için bir snapshot
  kaydı oluşturulur (fetch+parse başarılıysa).
- AC-3: Hedeflerden biri fetch/parse hatası verirse, o hedef için snapshot oluşmaz ama
  diğer hedefler için toplama normal şekilde devam eder ve tamamlanır.
- AC-4: Bir hedefin snapshot geçmişi zaman sırasına göre (eskiden yeniye) sorgulanabilir.
- AC-5: Bir hedef silindiğinde, o hedefe ait daha önce kaydedilmiş snapshot'lar
  veritabanında kalmaya devam eder (kaybolmaz).

## Verification Evidence
- AC-1↔`test_add_and_list_target_roundtrip_ac1`, AC-2↔`test_collect_target_saves_snapshot_on_success_ac2`, AC-3↔`test_collect_target_no_snapshot_on_parse_failure_ac3`+`test_collect_all_continues_after_one_target_fails_ac3`, AC-4↔`test_get_history_returns_snapshots_oldest_first_ac4`, AC-5↔`test_delete_target_keeps_existing_snapshots_ac5`.
- Sonuç: 6/6 test yeşil (`pytest tests/test_store.py tests/test_collect.py`).
- Mutasyon muhakemesi: `collect.py`'de `except WebScraperError` bloğu kaldırılsa AC-3 testi kırmızı olur (exception fırlar, "failed" dönmez); `store.py`'de `delete_target` sorgusu `snapshots` tablosunu da siliyor şekilde değiştirilse AC-5 testi kırmızı olur.

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
