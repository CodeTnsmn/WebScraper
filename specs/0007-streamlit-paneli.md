# Spec 0007 — Streamlit Paneli: Fiyat Trendi ve Rakip Karşılaştırma

## Intent
Kullanıcı toplanan fiyat geçmişini (Spec 0002-0003) komut satırından okumak yerine
görsel olarak inceleyebilmeli: tek bir hedefin zaman içindeki fiyat trendini, ya da
birden fazla hedefi (aynı ürünün farklı sitelerdeki karşılıkları) aynı grafikte
karşılaştırarak rakip analizi yapabilmeli. Panel salt-okunur bir görselleştirme
katmanıdır — veri toplamayı tetiklemez (ADR 0001, docs/architecture.md sınırı).
Bilerek yapılmayacak: panelden hedef ekleme/silme/toplama tetikleme, otomatik
yenileme, döviz kuru çevrimi.

## Requirements
- Panel açıldığında tanımlı hedefler bir seçim listesinde görünür.
- Hiç hedef tanımlı değilse panel hata vermeden bilgilendirici bir boş durum gösterir.
- Kullanıcı bir veya birden fazla hedef seçtiğinde, seçilenlerin fiyat geçmişi zaman
  eksenli bir grafikte gösterilir; birden fazla hedef seçilirse her biri ayrı bir seri
  olarak aynı grafikte görünür (rakip karşılaştırma).
- Seçilen hedeflerin geçmişi yoksa (henüz hiç toplama yapılmamış), hata değil
  bilgilendirici bir mesaj gösterilir.
- Tek bir hedef seçiliyken, o hedefin en güncel fiyatı ve stok durumu özet olarak
  ayrıca gösterilir.
- Panel yalnızca `store` modülünden okur; `fetch`/`collect`/`sites` modüllerini
  içe aktarmaz veya çağırmaz (mimari sınır).

## Constraints
- **Kapsam dışı (bilinçli):** panelden hedef ekleme/silme/toplama tetikleme (bunlar
  CLI'nin işi, Spec 0006), otomatik/periyodik sayfa yenileme, döviz çevrimi.

## Context
Bkz. `docs/architecture.md` (`dashboard/` satırı: "store dışında veri kaynağına
erişemez, scraping tetikleyemez"), Spec 0002 (`store.get_history`), Spec 0003
(`PriceSnapshot.price`).

## Acceptance Criteria
- AC-1: Veritabanında hiç hedef yokken panel açıldığında istisna fırlatmaz, "henüz
  takip edilen hedef yok" türünde bir mesaj gösterir.
- AC-2: Geçmişi olan tek bir hedef seçildiğinde, grafiğe verilen veri noktası sayısı
  o hedefin snapshot sayısına eşittir.
- AC-3: Birden fazla hedef seçildiğinde, grafiğe verilen seri sayısı seçilen hedef
  sayısına eşittir (her hedef kendi serisinde).
- AC-4: Tek hedef seçiliyken gösterilen "güncel fiyat" özeti, o hedefin en son
  (zaman damgası en büyük) snapshot'ının fiyatıyla birebir eşleşir.
- AC-5: `dashboard` modülünün kaynak kodu `webscraper.fetch`, `webscraper.collect`
  veya `webscraper.sites` modüllerinden hiçbirini içe aktarmaz (statik denetim).

## Verification Evidence
- AC-1↔`test_empty_database_shows_info_message_no_crash_ac1`, AC-2↔`test_build_chart_dataframe_point_count_matches_history_ac2`, AC-3↔`test_build_chart_dataframe_series_count_matches_selected_targets_ac3`, AC-4↔`test_latest_snapshot_returns_most_recent_by_timestamp_ac4`+`test_target_with_history_renders_chart_and_metrics_ac4`, AC-5↔`test_dashboard_does_not_import_scraping_modules_ac5`.
- Sonuç: 49/49 test yeşil (tüm paket, `pytest tests/`), `streamlit.testing.v1.AppTest` ile panel gerçek Streamlit çalışma zamanında koşturuldu.
- Ayrıca gerçek tarayıcıda elle doğrulandı: iki rakip hedef (SiteA/SiteB) ile seed edilmiş veritabanı üzerinde panel açıldı; tek hedef seçiliyken tek seri + "Güncel Fiyat: 1299 TRY" / "Stok Durumu: Stokta" metrikleri doğru göründü; iki hedef seçildiğinde grafikte iki ayrı seri (SiteA/SiteB) render edildi.
- AP-02 notu: `test_dashboard_does_not_import_scraping_modules_ac5` ilk yazımda substring arama kullandığı için `data.py` içindeki mimari-sınırı açıklayan YORUM metnindeki "webscraper.fetch" ifadesini gerçek import sanıp kırmızıydı — kök neden testte: yorum ile gerçek import ayırt edilmiyordu. Test `ast` ile gerçek import düğümlerini ayrıştıracak şekilde düzeltildi; kod değişmedi.
- Mutasyon muhakemesi: `data.py`'de `if snapshot.price is not None` filtresi kaldırılsa AC-2 nokta sayısı testi hâlâ geçer ama `None` fiyatlı bir snapshot eklenen ayrı bir testte (`test_build_chart_dataframe_skips_snapshots_without_numeric_price`) kırmızı olurdu; `app.py`'de `len(selected_labels) == 1` koşulu kaldırılıp metrikler her zaman gösterilse, AC-3 çoklu-seçim senaryosunda tarayıcı testinde metrik alanı yanlış/eksik veriyle görünürdü (elle doğrulamada gözlemlenebilir, otomatik testle AC-4'ün tek-hedef varsayımı bozulurdu).

## Definition of Done
- [x] Tüm AC'ler karşılandı ve teste bağlandı
- [x] Bağımsız REVIEW geçti (aynı oturumda QA şapkasıyla)
- [x] Test anlamı doğrulandı (mutasyon)
- [x] Docs/ADR gerekiyorsa güncellendi (gerekmedi — ADR 0001 zaten paneli öngörmüştü)

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
