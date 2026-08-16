# AP Kataloğu — Kurtarma Rampaları

> Bu katalog kod çözümü içinde tutulmaz; bir AP'nin TAM adımlarını Takım Yöneticisi
> (insan) ilgili oturumda çalıştırır. Bir ajan burada bir durumun bir AP'ye uyduğunu
> düşünüyorsa, kodu söyler ve yöneticiden tam talimatı ister. Amaç: bir şeyler ters
> gittiğinde doğaçlama düzeltme yapmak yerine, tanımlı ve güvenli bir rampadan dönmek.

| Kod | Durum | Temel Kural |
|---|---|---|
| AP-01 | Derleme/çalışma zamanı hatası | Önce TEŞHİS, sonra TEK düzeltme; semptomu susturmak (try/catch'e gömme, uyarı kapatma) yasak. |
| AP-02 | Test kırmızı | Önce karar ver: kod mu, test mi, spec mi yanlış; assert zayıflatma/silme/skip yasak. |
| AP-03 | Kararsız (flaky) test | Deterministikleştir (zaman/rastgelelik/sıra bağımlılığını gider); skip/retry yasak; kanıt: art arda 5 yeşil koşu. |
| AP-04 | Düzeltme regresyon yarattı | Önce GERİ AL, yeşile dön; sonra daha dar kapsamlı düzeltme + kalıcı regresyon testi. |
| AP-05 | "Araştırılacak" bulgu | Düzeltme değil MİNİMAL REPRO üret; repro yoksa gerekçeli kapanış. |
| AP-06 | Düzeltme tur sınırı aşıldı | DUR; kök neden spec'te mi plan'da mı — yalnızca analiz, kod yazma yok. |
| AP-07 | Plan dışına çıkıldı | Sapma listesi çıkar; onaysız değişiklik geri alınır. |
| AP-08 | İş ortasında spec/gereksinim değişti | Önce spec güncellenir → delta plan çıkarılır → onay beklenir. |
| AP-09 | Bağlam bulanıklaştı / oturum uzadı | Durum dosyası yaz (bitti/yarım/riskler) + oturum devri; kanıtsız "tamamlandı" yazılmaz. |
| AP-10 | Belirsizlik / docs-kod-spec çelişkisi | VARSAYMA; seçenekleri bedelleriyle getir, karar Takım Yöneticisinde. |
| AP-11 | Güvenli geri alma (migration/veri dahil) | git revert; history silme/force push yasak; önce risk raporu (veri kaybı var mı?) sunulur. |
| AP-12 | Performans hedefi tutmadı | Önce ÖLÇÜM (tahmin değil), TEK optimizasyon, aynı yöntemle yeniden ölç. |

## Oturum eşlemesi (öneri)
- AP-01, 02, 04, 06, 07, 08, 09, 10, 11, 12 → genelde **Developer** oturumunda tetiklenir ve çözülür.
- AP-05 → **QA** oturumunda çalışır — kendi kodunu yazan akıl "repro edemedim" demeye meyillidir.
- AP-03 → Developer deterministikleştirir; QA "art arda 5 yeşil" kanıtını bağımsız doğrular.
- AP-09 → mevcut oturumdan yeni oturuma devir; devralan oturum durum dosyasını okuyarak başlar.

## Ortak koruma kuralları (her AP için geçerli)
- Test silme/zayıflatma/skip yasak.
- Yalnızca ilgili dosyalara dokunulur — kapsam dışına taşma AP-07'yi tetikler.
- Her düzeltme çalıştırılmış test kanıtıyla döner, iddiayla değil.
- docs/spec, yapılan değişiklikle senkron tutulur.
