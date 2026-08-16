# Test Stratejisi

## Katmanlar
- **Unit:** `clean`, `parse` (sabit HTML fixture'larıyla), `export` — dış ağ çağrısı yok.
- **Integration:** `store` (gerçek SQLite, geçici dosya) + `schedule` tetikleme mantığı.
- **Site adaptör testleri:** her adaptör için kayıtlı örnek HTML fixture (`tests/fixtures/<site>.html`)
  üzerinden parse doğruluğu — canlı siteye test sırasında istek atılmaz.

## Adlandırma
`test_<modül>_<senaryo>.py` · fonksiyon `test_<davranış>_<beklenen_sonuç>`.

## Kurallar
- Canlı ağ isteği testte yasak (fixture/mock kullanılır) — testler hedef sitenin
  ayakta olmasına bağımlı olmaz.
- Fiyat/Decimal karşılaştırmalarında float tolerance yasak — Decimal eşitliği.
- Mutasyon muhakemesi: kritik testler VERIFY adımında "bu satırı bozsam kırmızı olur muydu" ile doğrulanır.
