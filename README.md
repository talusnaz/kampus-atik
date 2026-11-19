# Akıllı Kampüs Geri Dönüşüm ve Atık Doğrulama Sistemi

Kampüs içindeki geri dönüşüm kutularına yanlış atık atılmasını (kontaminasyonu) önleyen, barkod + statik kutu QR kodu + kutu içi sensör doğrulamalı web prototipi.

## Kurulum ve Çalıştırma
1. Gerekli kütüphaneleri yükleyin: `pip install -r requirements.txt`
2. Uygulamayı başlatın: `python app.py`
3. Tarayıcıdan `http://127.0.0.1:5001` adresine gidin.

# ♻️ Kampüs Atık — Akıllı Atık Ayrıştırma ve Karbon Tasarrufu Sistemi

Bu proje, İstinye Üniversitesi ve Erasmus+ Jean Monnet Modülü **EU-SMART** iş birliğiyle düzenlenen **Dijital Dönüşüm ve Sürdürülebilirlik Vaka Yarışması** (*Gıda ve Atık Kategorisi*) kapsamında geliştirilmiştir.

## 📌 Proje Özeti

Kampüs içindeki geri dönüşüm istasyonlarına yapılan hatalı atımları önlemek ve ayrıştırma sürecini ölçülebilir karbon tasarrufuna dönüştürmek amacıyla geliştirilen IoT tabanlı bir akıllı doğrulama sistemidir.

### Sistem Nasıl Çalışır?
1. **Barkod Okutma:** Kullanıcı, web arayüzü üzerinden elindeki atığın barkodunu okutur. Sistem atık türünü belirleyerek ilgili ayrıştırma bölmesini (**Sarı**, **Kırmızı** veya **Mavi**) aktif hale getirir.
2. **Fiziksel Algılama:** Atık, kullanıcının el müdahalesini önleyen içbükey kutu ağzından bırakıldığında ilgili bölmedeki kızılötesi (IR) mesafe sensörü hareketi algılar.
3. **Bulut İletişimi:** **NodeMCU ESP8266** mikrodenetleyicisi, Wi-Fi üzerinden buluttaki (**Render**) Python/Flask sunucusuna anlık `POST` isteği gönderir.
4. **Doğrulama ve Karbon Hesabı:** Sunucu, atığın beklenen doğru kutuya atıldığını doğrulayarak kampüsün net karbon tasarrufu ($CO_{2e}$) sayacını günceller; yanlış kutuya atılması durumunda ekranda anlık uyarı gösterir.

---

## 🛠️ Kullanılan Teknolojiler ve Donanım

* **Backend & Web Arayüzü:** Python, Flask, HTML/CSS/JavaScript (Render bulut sunucusu üzerinde yayında)
* **Donanım & IoT:** NodeMCU V3 ESP8266 (ESP-12E), 3 adet 2–20 cm Kızılötesi (IR) Mesafe Sensörü, Mini Breadboard, Jumper Kablolar

---

## 🚀 Kurulum ve Çalıştırma Adımları

### 1. Web Uygulamasını Yerelde Çalıştırma
```bash
git clone [https://github.com/talusnaz/kampus-atik.git](https://github.com/talusnaz/kampus-atik.git)
cd kampus-atik
pip install -r requirements.txt
python app.py
```
*(Not: Prototip arayüzü Render bulut sunucusu üzerinde canlı olarak da erişime açıktır.)*

### 2. Donanım Bağlantısı ve ESP8266 Kurulumu
* **Sensör 1 (Sarı Kutu):** NodeMCU `D1` pini
* **Sensör 2 (Kırmızı Kutu):** NodeMCU `D2` pini
* **Sensör 3 (Mavi Kutu):** NodeMCU `D5` pini
* **Güç Hatları:** Tüm sensörlerin `VCC` ve `GND` uçları breadboard üzerinden ortak hatta bağlanır.
* Arduino IDE üzerinden NodeMCU kartına 2.4 GHz Wi-Fi ağ bilgileri ve Render API uç noktası tanımlanarak donanım kodu yüklenir.

---

## 👥 Ekip Üyeleri ve Görev Dağılımı

* **Furkan Kartal** *(İstinye Üniversitesi — Yönetim Bilişim Sistemleri)*: Yazılım Geliştirme, IoT Donanım Entegrasyonu ve Sistem Mimarisi
* **Efe** *(İstinye Üniversitesi — Yönetim Bilişim Sistemleri)*: Donanım Kurulumu, Sistem Testleri ve Teknik Entegrasyon
* **Elif** *(İstinye Üniversitesi — Psikoloji)*: Karbon Etki Analizi, Veri Araştırması ve Kullanıcı Davranışı Tasarımı
* **İrem** *(İstinye Üniversitesi — Psikoloji)*: Fiziksel Prototip Tasarımı, Kullanıcı Deneyimi ve Sunum Süreci

---

## 🤖 Yapay Zekâ Kullanım Beyanı

Geliştirme sürecinde yazılım mimarisi optimizasyonu, dokümantasyon düzenlemesi ve kod hata ayıklama adımlarında üretken yapay zekâ araçlarından yararlanılmıştır. bunun devamını doldurun lütfen unutmayın arkadaşlar 
