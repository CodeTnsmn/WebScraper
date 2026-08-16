# Spec 0004 — CSV / Excel / Veritabanına Aktarma

## Intent
Toplanan fiyat verisi (Spec 0002/0003) zaten SQLite'ta kalıcı (veritabanına aktarma
bu şekilde zaten karşılanıyor — bkz. Context). Kullanıcının bu veriyi Excel'de analiz
edebilmesi veya başka araçlara aktarabilmesi için CSV ve Excel dosyası olarak
dışa aktarabilmesi gerekiyor. Bilerek yapılmayacak: PDF/başka format dışa aktarma,
export sırasında veri dönüştürme/filtreleme (ham export — filtreleme ileride ayrı
bir ihtiyaç olursa yeni spec).

## Requirements
- Bir hedefin veya tüm hedeflerin fiyat geçmişi CSV dosyasına aktarılabilmeli.
- Aynı veri Excel (.xlsx) dosyasına aktarılabilmeli.
- Dışa aktarılan dosyada en az şu kolonlar bulunmalı: hedef adı, zaman damgası, ham
  fiyat metni, sayısal fiyat, para birimi, stok durumu.
- Aktarılacak snapshot yoksa (boş geçmiş), hata fırlatmadan yalnızca başlık satırı
  olan boş bir dosya üretilmeli.
- Var olan bir export dosyasının üzerine tekrar export edilirse, dosya sessizce
  güncel veriyle değiştirilmeli (üzerine yazma, hata değil).

## Constraints
- **Kapsam dışı (bilinçli):** PDF export, export sırasında tarih aralığı filtresi
  (ihtiyaç doğarsa ayrı bir spec ile eklenir).

## Context
Veritabanına aktarma zaten Spec 0002'de `store.py` (SQLite) ile karşılanıyor; bu
spec yalnızca CSV/Excel dosya çıktısını ekler. Bkz. `docs/architecture.md` (`export`
modülü, yalnızca `store`'dan okur).

## Acceptance Criteria
- AC-1: Snapshot'ları olan bir hedef CSV'ye aktarıldığında, dosyadaki satır sayısı
  snapshot sayısına eşittir ve her satırda hedef adı, zaman damgası, ham fiyat,
  sayısal fiyat, para birimi, stok durumu doğru sırayla yer alır.
- AC-2: Aynı veri Excel'e aktarıldığında, açılan çalışma sayfasındaki değerler CSV
  ile aynıdır (satır/kolon eşleşir).
- AC-3: Snapshot geçmişi boş olan bir hedef export edildiğinde hata fırlatılmaz;
  yalnızca başlık satırını içeren bir dosya oluşur.
- AC-4: Tüm hedefler tek seferde export edildiğinde, çıktı dosyasında her hedefin
  tüm snapshot'ları yer alır (hedef bazında filtrelenmiş export'un birleşimi).
- AC-5: Var olan bir dosya yolu tekrar export edilirse dosya üzerine yazılır (eski
  içerik kalıntısı kalmaz) — hata fırlatılmaz.

## Verification Evidence
- AC-1↔`test_export_csv_row_count_and_columns_ac1`, AC-2↔`test_export_excel_matches_csv_ac2`, AC-3↔`test_export_empty_history_writes_header_only_ac3`, AC-4↔`test_export_all_targets_includes_every_target_ac4`, AC-5↔`test_export_overwrites_existing_file_ac5`.
- Sonuç: 30/30 test yeşil (tüm paket, `pytest tests/`).
- Mutasyon muhakemesi: `export.py`'de `columns=COLUMNS` parametresi kaldırılsa AC-3 testi kırmızı olur (boş DataFrame'de kolon başlıkları kaybolur, sadece boş dosya çıkar); `store.py`'de LEFT JOIN yerine INNER JOIN kullanılsa silinmiş hedefin snapshot'ları export'tan düşer (domain.md ihlali) — ayrı bir regresyon testiyle değil, kod incelemesiyle doğrulandı.

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
