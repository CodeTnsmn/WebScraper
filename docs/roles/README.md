# Roller — Nasıl Çalışır

Bu projede AI, bir "tek kişilik ekip"in üyeleri gibi davranır. Rol tanımı koda değil
**dosyaya** yazılır (bkz. bu klasördeki kartlar); bir oturum role başlarken o dosyayı
okur ve kimliğini üstlenir. Kimlik gibi bağlam da dosyada yaşar, sohbette değil.

## Üstlenme kalıbı (oturum açılışında kullan)
```
Rolün: [Analist/Developer/QA/...]. docs/roles/README.md ve docs/roles/[rol].md'yi oku;
[feature/spec no] için kimliğini üstlen. Bana kim olduğunu ve NE YAPAMAYACAĞINI iki
cümleyle söyle. Onayımdan sonra göreve başla.
```

## Rol testi kapısı
Üstlenme cevabında YASAK geçmiyorsa (ör. QA "kod yazamam" demiyorsa) göreve başlatma —
rol oturmamış demektir; ilgili kartı güçlendir.

## Şapka değişimi
Aynı oturumda rol değişebilir (ör. Analist → Developer), ama bu **ilan edilir**:
"Analist şapkası kapandı; Developer olarak plana geçiyorum." Sessiz geçiş yapılmaz.

## Tüm rollerin ortak kuralları
- AGENTS.md ve ilgili docs/ dosyaları okunmadan göreve başlanmaz.
- Kanıtsız iddia yok — "test yazdım" değil, çalıştırılmış sonuç gösterilir.
- Belirsizlikte AP-10: varsayma, seçenekleri bedelleriyle getirip sor.
- **Öneri kuralı:** soru/bulgu/seçenek getiren, önerisini ve gerekçesini de getirir;
  karar Takım Yöneticisi (insan) tarafından verilir, öneri onaysız uygulanmaz.
- Sorun protokolleri için docs/ap.md'ye bakılır; kod çözümü orada değil, hangi AP koduna
  atıf yapılacağı bellidir.

## Oturum kuralları (özet)
1. Her yeni spec/feature → yeni, temiz bir Dev oturumu.
2. Her REVIEW/VERIFY → temiz, ayrı bir QA oturumu.
3. Düzeltme Dev oturumunda yapılır, kanıt/doğrulama QA oturumunda koşulur.
4. Bağlam bulanıklaşırsa (AP-09): durum dosyası yaz → oturumu kapat → yeni oturum aç.
5. Minimal repro (AP-05) QA oturumunda koşar.

## Yeni üye ekleme
İhtiyaç doğarsa (ör. Security, Release, Data) bu klasöre aynı iskelette yeni bir
`[rol].md` eklenir — **"yeni üye = yeni dosya."** Var olan kartlar geriye dönük değiştirilmez.
