# Sigarayı Bırakma Yardımcısı

Bu proje, sigarayı bırakma sürecinde olan kullanıcılara motivasyon sağlamak ve ilerlemelerini takip etmelerine yardımcı olmak amacıyla Python ve KivyMD kütüphaneleri kullanılarak geliştirilmiş modüler bir mobil uygulamadır.

Uygulama, kullanıcıya hem sayısal verilerle hem de motive edici özelliklerle destek olmayı hedefler.

![Uygulama Ana Ekran Görüntüsü](https://i.imgur.com/n1g7i4a.png)


## ✨ Özellikler

Uygulamamız, sigarayı bırakma yolculuğunu desteklemek için zengin bir özellik setine sahiptir:

* **Dinamik Gösterge Paneli:**
    * Sigarasız geçen gün sayısı.
    * Tasarruf edilen para miktarı.
    * İçilmeyen toplam sigara adedi.
    * Geri kazanılan tahmini yaşam süresi.
* **Motivasyon Araçları:**
    * Her açılışta değişen ilham verici sözler.
    * Kullanıcının kendi girdiği kişisel bırakma nedenlerinin hatırlatılması.
    * **Sağlık Gelişimi Takibi:** Bıraktıktan sonra vücutta meydana gelen olumlu değişiklikleri gösteren zaman çizelgesi.
    * **Başarılar ve Rozetler:** Belirli hedeflere (geçen gün, biriktirilen para vb.) ulaşıldığında kazanılan görsel rozetler.
* **İnteraktif Destek:**
    * **Kriz Anı Butonu:** Sigara içme arzusu geldiğinde anında destek sağlayan bir panik butonu.
    * **Kriz Günlüğü:** Kriz anlarının ne zaman yaşandığını kaydeden ve listeleyen bir günlük.
* **Bilgi ve Eğitim:**
    * **Yoksunluk Belirtileri Ekranı:** Karşılaşılabilecek olası yoksunluk belirtileri ve başa çıkma ipuçları hakkında bilgi.
* **Kişiselleştirme:**
    * Kişisel sigara alışkanlıklarını (günlük adet, paket fiyatı) kaydetme.
    * Açık ve Koyu tema arasında geçiş yapma ve seçimi hatırlama.

## 🛠️ Kullanılan Teknolojiler

* **Programlama Dili:** Python 3
* **Arayüz (UI) Kütüphanesi:** Kivy & KivyMD
* **Veritabanı:** SQLite 3 (Python'un dahili modülü)

## 🚀 Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin:

1.  **Projeyi Klonlayın (veya dosyaları indirin):**
    ```bash
    git clone [https://github.com/kullanici-adiniz/sigarayi-birakma-uygulamasi.git](https://github.com/kullanici-adiniz/sigarayi-birakma-uygulamasi.git)
    cd sigarayi-birakma-uygulamasi
    ```

2.  **Sanal Ortam Oluşturun (Tavsiye Edilir):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux için
    .\venv\Scripts\activate   # Windows için
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    Proje klasöründe aşağıdaki içeriğe sahip bir `requirements.txt` dosyası oluşturun:
    ```
    kivy
    kivymd
    ```
    Ardından bu komutu çalıştırın:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uygulamayı Çalıştırın:**
    ```bash
    python main.py
    ```

## 📁 Proje Yapısı

Uygulama, bakımı ve geliştirmesi kolay, modüler bir yapıda tasarlanmıştır:
sigarayi_birak_app/
|
├── assets/                 # İkonlar ve rozetler gibi statik dosyalar
|   ├── badges/
|   └── icons/
|
├── core/                   # Uygulamanın ana mantığı ve veri dosyaları
|   ├── init.py
|   ├── badges_data.py
|   ├── health_data.py
|   ├── quotes_data.py
|   ├── symptoms_data.py
|   └── tracker.py
|
├── database/               # Veritabanı yönetimi
|   ├── init.py
|   └── db_manager.py
|
├── screens/                # Arayüz ekranları
|   ├── init.py
|   ├── achievements_screen.py
|   ├── craving_log_screen.py
|   ├── home_screen.py
|   ├── settings_screen.py
|   └── symptoms_screen.py
|
└── main.py                 # Uygulamanın başlangıç dosyası


## 🔮 Gelecek Planları

* Uygulamayı **Buildozer** ile `.apk` (Android) ve `.ipa` (iOS) formatlarına paketlemek.
* Belirli başarılara ulaşıldığında motive edici bildirimler göndermek.
* Kriz günlüğü verilerini analiz edip kullanıcıya kişisel raporlar sunmak.
