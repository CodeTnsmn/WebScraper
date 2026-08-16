# ADR 0001: Uygulama Formatı — CLI+Kütüphane Çekirdek, Opsiyonel Streamlit Panel

**Durum:** Kabul
**Tarih:** 2026-08-16

## Bağlam
Proje e-ticaret fiyat takibi ve rakip analizi yapan bir web scraper. İstenen özellikler:
hedef sitelerden veri çıkarma, otomatik toplama, veri temizleme, CSV/Excel/DB'ye aktarma,
zamanlanmış çalıştırma. Kullanıcı uygulamanın "app" formatında mı yoksa başka türlü mü
olacağına karar verilmesini istedi.

## Karar
Çekirdek iş mantığı (scraping, temizleme, depolama, zamanlama) bağımsız bir Python
kütüphanesi + CLI olarak yazılır (`src/webscraper/`). Görselleştirme/rakip karşılaştırma
ihtiyacı için üstüne ince bir **Streamlit paneli** eklenir (opsiyonel katman, çekirdeğe
bağımlı değil, çekirdek panelsiz de tam çalışır). Zamanlanmış çalıştırma önce
kütüphane-içi scheduler (APScheduler) ile sağlanır; işletim sistemi görev zamanlayıcısı
(Windows Task Scheduler / cron) ile tetikleme dokümante edilir, zorunlu kılınmaz.

## Sonuçlar
**İyi yanları:**
- Scraping/scheduling arka plan işi CLI'dan bağımsız test edilebilir, sunucu gerektirmez.
- Panel opsiyonel olduğu için "sadece veri lazım" senaryosunda gereksiz ağırlık yok.
- Rakip fiyat karşılaştırma/görselleştirme ihtiyacı panelle karşılanır.

**Bedeli:**
- İki giriş noktası bakımı (CLI + panel) — ama panel çekirdeğe ince bir katman.

## Değerlendirilen Alternatifler
1. **Sadece CLI/script, panel yok** — rakip analizi görselleştirme ihtiyacını karşılamaz.
2. **Tam web uygulaması (FastAPI + frontend)** — kapsam fazlası; tek kullanıcı/lokal
   kullanım senaryosunda gereksiz altyapı yükü (auth, deploy, API katmanı).

## İlgili
Bkz. `docs/architecture.md`. Bu karar ileride çoklu-kullanıcı/hosted ihtiyaç doğarsa
gözden geçirilir.
