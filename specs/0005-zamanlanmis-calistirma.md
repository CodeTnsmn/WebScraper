# Spec 0005 — Zamanlanmış Çalıştırma

## Intent
Kullanıcı fiyat toplamayı elle her seferinde tetiklemek istemiyor; belirlediği aralıkla
(ör. her 60 dakikada bir) otomatik tekrar etmesini istiyor. Bir toplama turunda hata
oluşması (ör. bir hedefin sitesi geçici olarak erişilemez), zamanlayıcının kendisini
durdurmamalı — bir sonraki tur yine planlandığı gibi çalışmalı. Bilerek yapılmayacak:
işletim sistemi seviyesinde (Windows Task Scheduler/cron) kurulum otomasyonu — bu
kütüphane-içi zamanlayıcıyı sağlar, OS entegrasyonu dokümantasyonla anlatılır.

## Requirements
- Kullanıcı, "her X dakikada bir topla" şeklinde bir zamanlayıcı kurabilmeli.
- Zamanlayıcı kurulduğunda, istenirse ilk toplama turu beklemeden hemen başlatılabilmeli
  (opsiyonel "hemen çalıştır" davranışı).
- Zamanlanmış bir toplama turunda beklenmeyen bir hata oluşursa, bu hata zamanlayıcının
  çalışmaya devam etmesini engellememeli.
- Zamanlayıcı durdurulduğunda artık yeni tur tetiklenmemeli.
- Zamanlayıcı, hangi toplama işinin çalıştırılacağından bağımsız olmalı (parsing/export
  mantığı zamanlayıcı modülüne sızmamalı — bkz. docs/architecture.md).

## Constraints
- **Kapsam dışı (bilinçli):** OS görev zamanlayıcısı entegrasyonu (Task
  Scheduler/cron) — yalnızca dokümante edilir, kod yazılmaz; birden fazla eşzamanlı
  zamanlayıcı örneği/dağıtık kilitleme (tek-proses kullanım varsayımı).

## Context
Bkz. `docs/architecture.md` (`schedule` modülü). `collect_all` (Spec 0002) zamanlanan
işin gövdesi olarak kullanılacak ama `schedule` modülü ona doğrudan bağımlı değildir —
herhangi bir çağrılabilir (`job_func`) kabul eder.

## Acceptance Criteria
- AC-1: X dakikalık aralıkla kurulan zamanlayıcının işi, tam olarak X dakikalık
  bir tetikleyiciye (interval trigger) sahiptir.
- AC-2: Zamanlayıcının işi tetiklendiğinde, verilen toplama fonksiyonu çağrılır.
- AC-3: "Hemen çalıştır" seçeneği açıkken kurulan zamanlayıcının ilk çalışma zamanı
  şimdiye çok yakındır (ilk aralığı beklemez); kapalıyken ilk çalışma zamanı yaklaşık
  bir aralık sonrasıdır.
- AC-4: Toplama fonksiyonu çalışırken bir istisna fırlatırsa, bu istisna zamanlayıcı
  sürecine yayılmaz (zamanlayıcı ayakta kalır).
- AC-5: Zamanlayıcı durdurulduktan sonra `running` durumu false olur.

## Verification Evidence
- AC-1↔`test_interval_trigger_matches_requested_minutes_ac1`, AC-2↔`test_job_func_triggers_registered_callable_ac2`, AC-3↔`test_run_immediately_schedules_close_to_now_ac3`+`test_without_run_immediately_first_run_is_about_one_interval_away_ac3`, AC-4↔`test_exception_in_job_is_swallowed_by_wrapper_ac4`, AC-5↔`test_shutdown_sets_running_false_ac5`.
- Sonuç: 36/36 test yeşil (tüm paket, `pytest tests/`).
- AP-02 notu: `test_without_run_immediately_first_run_is_about_one_interval_away_ac3` ilk yazımda `AttributeError: 'Job' object has no attribute 'next_run_time'` ile kırmızıydı — kök neden kodda değil testte: APScheduler `next_run_time`'ı yalnızca scheduler start edildikten sonra hesaplıyor (pending job'da yok). Test, okumadan önce `sched.start()` çağıracak şekilde düzeltildi; kod değişmedi.
- Mutasyon muhakemesi: `schedule.py`'de `_crash_resilient` wrapper'ı kaldırılsa AC-4 testi kırmızı olur (RuntimeError doğrudan fırlar); `run_immediately` dalındaki `next_run_time` ataması silinse AC-3'ün immediate testi kırmızı olur (next_run_time ~30 dakika sonrasına düşer).

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
