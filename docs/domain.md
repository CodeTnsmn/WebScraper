# Alan Sözlüğü ve İş Kuralları

## Terimler
- **Hedef (Target):** Takip edilen bir ürünün belirli bir sitedeki URL'i.
- **Site Adaptörü:** Bir e-ticaret sitesinin HTML yapısına özel parse mantığı.
- **Snapshot:** Bir hedefin belirli bir zamandaki fiyat/stok/durum kaydı.
- **Rakip Analizi:** Aynı ürünün farklı sitelerdeki snapshot'larının karşılaştırılması.

## İş Kuralları
- Fiyat her zaman `Decimal` tutulur, `float` yasak (yuvarlama hatası riski).
- Para birimi her snapshot'ta ayrı alan olarak tutulur, varsayım yapılmaz.
- Bir hedef silinse bile geçmiş snapshot'lar saklanır (fiyat geçmişi kaybolmaz).
- Scraping yalnızca herkese açık, oturum/login gerektirmeyen ürün sayfalarını hedefler.
- Her site adaptörü `robots.txt`'e uyar; disallow edilen path'ler taranmaz.
- İstekler arası bekleme (rate-limit) zorunlu; hedef siteye yük bindirilmez.

## Kapsam Dışı (bilinçli)
- Login gerektiren/özel fiyat sayfaları — yetkisiz erişim riski.
- CAPTCHA bypass — yasak, uygulanmaz.
- Kişisel veri toplama — yalnızca ürün/fiyat verisi toplanır.
