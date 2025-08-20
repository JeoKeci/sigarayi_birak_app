# screens/settings_screen.py

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDTextButton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDSwitch
from datetime import datetime
# YENİ: Plyer kütüphanesinden email özelliğini içe aktarıyoruz
from plyer import email

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quit_date = None

        root_layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(title="Ayarlar", left_action_items=[["arrow-left", lambda x: self.go_back()]], elevation=4,)
        root_layout.add_widget(toolbar)
        content_layout = MDBoxLayout(orientation='vertical', padding="20dp", spacing="20dp",)

        self.cigarettes_per_day_field = MDTextField(hint_text="Günde içilen sigara adedi", input_filter="int")
        self.price_per_pack_field = MDTextField(hint_text="Bir paket sigara fiyatı (₺)", input_filter="float")
        
        self.reasons_field = MDTextField(
            hint_text="Bırakma Nedenlerim (her satıra bir tane)",
            multiline=True,
            height="100dp"
        )

        theme_layout = MDBoxLayout(adaptive_height=True, padding=("0dp", "12dp", "0dp", "12dp"))
        theme_label = MDLabel(text="Koyu Tema")
        self.theme_switch = MDSwitch()
        theme_layout.add_widget(theme_label)
        theme_layout.add_widget(self.theme_switch)

        date_button = MDRaisedButton(text="Bırakma Tarihini Seç", on_release=self.show_date_picker, pos_hint={'center_x': 0.5})
        save_button = MDRaisedButton(text="Kaydet", on_release=self.save_data, pos_hint={'center_x': 0.5})
        
        privacy_button = MDTextButton(
            text="Gizlilik Politikası",
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.go_to_privacy_policy()
        )
        
        # YENİ: Geri Bildirim Butonu
        feedback_button = MDTextButton(
            text="Geri Bildirim Gönder",
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.send_feedback_email()
        )

        content_layout.add_widget(self.cigarettes_per_day_field)
        content_layout.add_widget(self.price_per_pack_field)
        content_layout.add_widget(self.reasons_field)
        content_layout.add_widget(theme_layout)
        content_layout.add_widget(date_button)
        content_layout.add_widget(save_button)
        content_layout.add_widget(feedback_button) # Yeni butonu ekliyoruz
        content_layout.add_widget(privacy_button)
        
        root_layout.add_widget(content_layout)
        self.add_widget(root_layout)

    # --- YENİ FONKSİYON ---
    def send_feedback_email(self):
        try:
            email.send(
                recipient='karakas.halil@gmail.com', # Kendi e-posta adresinizi buraya yazın
                subject='Bırakma Yardımcısı - Geri Bildirim',
                text='Merhaba,\n\nUygulama hakkındaki geri bildirimim aşağıdadır:\n\n'
            )
        except Exception as e:
            # Telefonda e-posta uygulaması kurulu değilse veya bir hata olursa
            snackbar = MDSnackbar()
            snackbar.text = "E-posta uygulaması açılamadı."
            snackbar.open()
            print(f"E-posta gönderme hatası: {e}")
    # ---------------------------

    def on_enter(self):
        app = MDApp.get_running_app()
        profile = app.db_manager.load_user_profile()
        if profile:
            quit_date, cigs_per_day, price_per_pack, theme_style, personal_reasons = profile
            self.cigarettes_per_day_field.text = str(cigs_per_day)
            self.price_per_pack_field.text = str(price_per_pack)
            self.reasons_field.text = personal_reasons if personal_reasons else ""
            self.quit_date = datetime.strptime(quit_date, '%Y-%m-%d')
            self.theme_switch.active = True if theme_style == "Dark" else False

    def go_back(self):
        self.manager.current = 'home'
        
    def go_to_privacy_policy(self):
        self.manager.current = 'privacy_policy'

    def show_date_picker(self, instance):
        date_dialog = MDDatePicker()
        if self.quit_date:
            date_dialog.set_date(self.quit_date)
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()

    def on_date_save(self, instance, value, date_range):
        self.quit_date = value
        snackbar = MDSnackbar()
        snackbar.text = f"Tarih seçildi: {self.quit_date.strftime('%d-%m-%Y')}"
        snackbar.open()

    def save_data(self, instance):
        cigs_per_day = self.cigarettes_per_day_field.text
        price_per_pack = self.price_per_pack_field.text
        
        if not cigs_per_day or not price_per_pack or not hasattr(self, 'quit_date') or not self.quit_date:
            snackbar = MDSnackbar()
            snackbar.text = "Lütfen tüm alanları doldurun ve tarih seçin!"
            snackbar.open()
            return
        
        app = MDApp.get_running_app()
        quit_date_str = self.quit_date.strftime('%Y-%m-%d')
        theme_style = "Dark" if self.theme_switch.active else "Light"
        personal_reasons = self.reasons_field.text
        
        app.db_manager.save_user_profile(
            quit_date=quit_date_str,
            cigarettes_per_day=int(cigs_per_day),
            price_per_pack=float(price_per_pack),
            theme_style=theme_style,
            personal_reasons=personal_reasons
        )
        
        app.change_theme(theme_style)
        snackbar = MDSnackbar()
        snackbar.text = "Ayarlar başarıyla kaydedildi!"
        snackbar.open()
        self.go_back()