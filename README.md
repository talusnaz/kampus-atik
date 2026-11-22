♻️ Kampüs Atık — Akıllı Atık Ayrıştırma ve Karbon Tasarrufu Sistemi
Bu proje, İstinye Üniversitesi İşletme Bölümü ve Erasmus+ Jean Monnet Modülü EU-SMART iş birliğiyle düzenlenen Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması (1. Gıda ve Atık Kategorisi, 23 Kasım 2026) kapsamında geliştirilmiştir.   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 2
Kampüs içindeki geri dönüşüm kutularına yanlış atık atılmasını (kontaminasyonu) önlemek ve ayrıştırma sürecini ölçülebilir karbon tasarrufuna dönüştürmek amacıyla geliştirilen IoT ve web tabanlı akıllı doğrulama prototipidir.   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 1
Canlı Çalışan Prototip: https://kampus-atik.onrender.com   
IMG_3122.jpg
+ 2
GitHub Deposu: https://github.com/talusnaz/kampus-atik.git
📌 Proje Özeti ve Çözüm Mantığı
Hangi Sorunu ve Kaynağı Azaltıyor?
Kampüs geri dönüşüm istasyonlarına atılan ambalajların yanlış bölmeye bırakılması, temiz geri dönüştürülebilir malzemelerin kirlenerek çöpe gitmesine yol açmaktadır. Sistemimiz; yanlış ayrıştırılan ambalaj atığı kontaminasyonunu, geri kazanılabilir ham madde kaybını ve buna bağlı karbon emisyonunu (
CO
2
 e
s
¸
d.
CO 
2
​	
  e 
s
¸
​	
 d.) azaltır.   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 1
Neden Dijital?
Sabit afişler ve renkli kutu etiketleri kullanıcıyı atım anında yönlendiremediği ve hatalı atımı engelleyemediği için tek başına yetersiz kalmaktadır. Bu dijital çözüm; barkod tanıma, sensör tabanlı fiziksel doğrulama ve anlık Yeşil Puan ödüllendirmesini birleştirerek davranışı atım anında doğrular.   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 1
Sistem Nasıl Çalışır?
Barkod Okutma: Kullanıcı, mobil web arayüzü üzerinden elindeki ambalajın barkod fotoğrafını çeker (html5-qrcode ve RapidOCR ile okunur) veya barkod numarasını manuel girer. Sistem, T.C. Sıfır Atık renk koduna göre doğru bölmeyi (Sarı, Gri veya Yeşil) ekranda gösterir.
Sensör Aktivasyonu ve Fiziksel Algılama: Kullanıcı "Sensörü Başlat" butonuna bastıktan sonra atığı ilgili bölmeye bırakır; bölme girişindeki kızılötesi (IR) mesafe sensörü atık geçişini algılar.
Bulut İletişimi: NodeMCU V3 ESP8266 (ESP-12E) mikrodenetleyicisi, Wi-Fi üzerinden buluttaki (Render) Python/Flask sunucusuna anlık POST isteği gönderir.
Doğrulama, Karbon Hesabı ve Yeşil Puan: Sunucu, atığın beklenen doğru kutuya atıldığını doğrulayarak kurtarılan temiz atık kütlesini (g), önlenen karbon tasarrufunu (
CO
2
CO 
2
​	
 ) ve kampüs kantini/kırtasiye kampanyalarında kullanılabilen Yeşil Puan sayacını günceller; yanlış kutuya atılması durumunda kontaminasyon uyarısı vererek puan yüklemez.
AB ve Döngüsel Ekonomi Bağlantısı (EU-SMART)
Sistem, ürün barkodunu bir Dijital Ürün Pasaportu anahtarı gibi kullanarak ambalajın malzeme türünü, net kütlesini ve geri dönüşüm akışını son kullanıcı noktasında görünür kılar; temiz ham madde geri kazanımını artırarak döngüsel ekonomiye doğrudan katkı sağlar.   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 1
📊 Ölçülebilir Çevresel Etki Hesabı ve Varsayımlar
Tek istasyonluk Vadi Kampüsü pilot senaryosu için yıllık net etki şu adımlarla hesaplanmıştır:   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 1
Pilot Ölçek ve Davranış Değişimi: Günlük 200 aktif öğrenci 
×
× 160 akademik gün 
×
× kişi başı önlenen 1,0 hatalı atım (1,50 → 0,50 adet/gün) = 32.000 adet/yıl kurtarılan ambalaj.   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
Kampüs Tüketim Dağılımı (Gerekçeli Örnek Varsayım): %55 PET Su (36,0 g CO₂), %20 Metal Kutu (135,0 g CO₂), %20 Atıştırmalık Paketi (5,76 g CO₂ ort.), %5 Cam Şişe (45,0 g CO₂) 
→
→ Ağırlıklı ortalama 50,20 g 
CO
2
CO 
2
​	
 /adet ve 22,14 g/adet.   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 1
Kurtarılan Temiz Ambalaj Kütlesi: 708,48 kg/yıl (352,00 kg PET, 240,00 kg Cam, 96,00 kg Metal, 20,48 kg Esnek Plastik).
Brüt Karbon Tasarrufu: 1.606,46 kg 
CO
2
CO 
2
​	
 /yıl.
Sistemin Kendi Enerji ve Bulut Ayak İzi: − 11,10 kg 
CO
2
CO 
2
​	
 /yıl (NodeMCU ESP8266 + 3 IR sensör ve Render bulut sunucusunun yıllık ~24,67 kWh tüketimi brüt kazançtan düşülmüştür).   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 1
Net Yıllık Karbon Kazancı: 1.595,36 kg 
CO
2
 e
s
¸
d./yıl
CO 
2
​	
  e 
s
¸
​	
 d./yıl (%99,31 Net Pozitif Etki). (Tüm ürünlerin eşit %12,5 atıldığı en muhafazakâr senaryoda dahi net kazanç 968,10 kg CO₂/yıl olarak pozitiftir.)   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
+ 2
Kullanılan Veri Kaynakları:
EPA WARM v16 (Waste Reduction Model): Malzeme bazlı geri dönüşüm emisyon faktörleri (Metal: 9,0 g CO₂/g, Plastik: 1,8 g CO₂/g, Cam: 0,3 g CO₂/g).   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
Avrupa Çevre Ajansı (EEA): Avrupa ambalaj atığı ve yaşam döngüsü emisyon göstergeleri.   
Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması.pdf
T.C. Enerji ve Tabii Kaynaklar Bakanlığı: Türkiye Ulusal Elektrik Şebekesi Emisyon Faktörü (0,45 kg CO₂/kWh).
🛠️ Kullanılan Teknolojiler ve Donanım
Backend & Web Arayüzü: Python, Flask, HTML5, Tailwind CSS, JavaScript (html5-qrcode), Pillow, RapidOCR (Render bulut sunucusu üzerinde yayında)
Donanım & IoT: NodeMCU V3 ESP8266 (ESP-12E), 3 adet 2–20 cm Kızılötesi (IR) Mesafe Sensörü, Mini Breadboard, Jumper Kablolar
🚀 Kurulum ve Çalıştırma Adımları
1. Web Uygulamasını Yerelde Çalıştırma
Depoyu klonlayın: git clone [https://github.com/talusnaz/kampus-atik.git](https://github.com/talusnaz/kampus-atik.git) ve cd kampus-atik komutlarıyla proje dizinine girin.
Gerekli kütüphaneleri yükleyin: pip install -r requirements.txt
Uygulamayı başlatın: python app.py
Tarayıcıdan [http://127.0.0.1:5001](http://127.0.0.1:5001) adresine gidin (veya doğrudan https://kampus-atik.onrender.com bağlantısından canlı demoyu test edin).   
IMG_3122.jpg
+ 2
2. Donanım Bağlantısı ve ESP8266 Pin Eşleştirmesi (Sıfır Atık Uyumlu)
Sarı Kutu (Plastik Atık): NodeMCU D5 pini (Sensör ID 2)
Gri Kutu (Metal Atık): NodeMCU D6 pini (Sensör ID 1)
Yeşil Kutu (Cam Atık): NodeMCU D7 pini (Sensör ID 3)
Güç Hatları: Tüm sensörlerin VCC ve GND uçları breadboard üzerinden ortak hatta bağlanır; Arduino IDE üzerinden NodeMCU kartına 2.4 GHz Wi-Fi ağ bilgileri ve Render API uç noktası (/api/esp32/check) tanımlanarak donanım kodu yüklenir.
👥 Ekip Üyeleri ve Görev Dağılımı
Furkan Kartal (İstinye Üniversitesi — Yönetim Bilişim Sistemleri): Yazılım Geliştirme, IoT Donanım Entegrasyonu ve Sistem Mimarisi
Efe (İstinye Üniversitesi — Yönetim Bilişim Sistemleri): Donanım Kurulumu, Sistem Testleri ve Teknik Entegrasyon
Elif (İstinye Üniversitesi — Psikoloji): Karbon Etki Analizi, Veri Araştırması ve Kullanıcı Davranışı Tasarımı
İrem (İstinye Üniversitesi — Psikoloji): Fiziksel Prototip Tasarımı, Kullanıcı Deneyimi ve Sunum Süreci
🤖 Yapay Zekâ Kullanım Beyanı
Geliştirme sürecinde yazılım mimarisi optimizasyonu, dokümantasyon düzenlemesi, karbon etki hesaplamalarının doğrulanması ve kod hata ayıklama adımlarında üretken yapay zekâ araçlarından; barkod görüntülerinin metne dönüştürülmesinde ise açık kaynaklı RapidOCR ve html5-qrcode kütüphanelerinden yararlanılmıştır.
