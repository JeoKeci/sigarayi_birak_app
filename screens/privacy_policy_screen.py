# screens/privacy_policy_screen.py

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel

# Metni, Kivy'nin biçimlendirme (markup) etiketleriyle birlikte hazırlıyoruz.
# [b]...[/b] -> Kalın, [size=...] -> Yazı tipi boyutu
PRIVACY_POLICY_TEXT = """
[size=18sp][b]Gizlilik Politikası[/b][/size]

[b]Son Güncelleme:[/b] 20 Ağustos 2025

Bu Gizlilik Politikası, [b]Sigarayı Bırak[/b] ("Uygulama") tarafından toplanan, kullanılan ve saklanan veriler hakkında sizi bilgilendirir.

[b]1. Toplanan Veriler[/b]

Uygulamamız, sigarayı bırakma sürecinizi kişiselleştirmek ve takip etmenize yardımcı olmak amacıyla aşağıdaki verileri toplar ve [b]yalnızca sizin kendi cihazınızda[/b] saklar:

* [b]Profil Bilgileriniz:[/b] Sigarayı bırakma tarihi, daha önce günde içtiğiniz sigara adedi, bir paket sigara fiyatı.
* [b]Kişisel Motivasyon Verileriniz:[/b] Sigarayı bırakmak için kendi yazdığınız kişisel nedenler.
* [b]Kullanım Kayıtlarınız:[/b] "Kriz Anı" butonuna bastığınız zaman damgaları ve günlük olarak girdiğiniz sigara adetleri.
* [b]Uygulama Ayarlarınız:[/b] Seçtiğiniz tema (Açık/Koyu).

[b]2. Verilerin Kullanım Amacı[/b]

Toplanan bu veriler, aşağıdaki amaçlar için kullanılır:

* Sigarasız geçen gün sayısını, tasarruf edilen parayı, içilmeyen sigara adedini ve kazanılan yaşam süresini hesaplamak ve size göstermek.
* Sağlık gelişimi hedeflerinize ve diğer başarılara ulaşıp ulaşmadığınızı takip etmek.
* Kriz anlarında size kendi kişisel nedenlerinizi hatırlatarak motivasyon sağlamak.
* Kriz anı ve günlük giriş verilerinizi analiz ederek size kişisel istatistikler sunmak.
* Uygulama arayüzünü (tema) tercihinize göre ayarlamak.

[b]3. Verilerin Saklanması ve Paylaşımı[/b]

[b]TÜM VERİLERİNİZ, YALNIZCA KENDİ MOBİL CİHAZINIZDA, UYGULAMAYA AİT GÜVENLİ ALANDA SAKLANIR.[/b]

* Uygulama tarafından toplanan hiçbir veri, geliştiricilere veya herhangi bir üçüncü parti sunucuya [b]gönderilmez, paylaşılmaz veya satılmaz.[/b]
* İnternet bağlantısı, sadece uygulamanın kendisini (veya kullandığı kütüphaneleri) güncellemek için gerekebilir; kişisel verileriniz asla transfer edilmez.

[b]4. Verilerin Silinmesi[/b]

Cihazınızda saklanan tüm verileri silmek için, telefonunuzun "Ayarlar > Uygulamalar > Bırakma Yardımcısı > Depolama" menüsünden "Verileri Temizle" seçeneğini kullanabilir veya uygulamayı tamamen kaldırabilirsiniz.

[b]5. İletişim[/b]

Gizlilik politikamızla ilgili herhangi bir sorunuz için lütfen bizimle iletişime geçin:
[b]karakas.halil@gmail.com[/b]
"""

class PrivacyPolicyScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root_layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(
            title="Gizlilik Politikası",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=4,
        )
        root_layout.add_widget(toolbar)

        scroll = MDScrollView()
        text_label = MDLabel(
            text=PRIVACY_POLICY_TEXT,
            markup=True,  # Metindeki [b] gibi etiketleri işlemesi için
            adaptive_height=True,
            padding="15dp"
        )
        scroll.add_widget(text_label)
        
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)

    def go_back(self):
        # Ayarlar ekranından geldiğimiz için oraya geri dönüyoruz.
        self.manager.current = 'settings'