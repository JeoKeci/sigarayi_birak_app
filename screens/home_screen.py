# screens/home_screen.py

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.button import MDTextButton, MDFillRoundFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDIcon
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from core.tracker import QuitTracker
from core.quotes_data import MOTIVATIONAL_QUOTES
import random
# DÜZELTME: timedelta import'u eklendi
from datetime import datetime, timedelta

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.panic_dialog = None
        self.daily_log_dialog = None

        root_layout = MDBoxLayout(orientation='vertical', spacing="10dp")

        toolbar = MDTopAppBar(
            title="",
            left_action_items=[
                ["notebook-edit-outline", lambda x: self.go_to_daily_log_history()]
            ],
            right_action_items=[
                ["history", lambda x: self.go_to_craving_log()],
                ["information-outline", lambda x: self.go_to_symptoms()],
                ["cog-outline", lambda x: self.go_to_settings()]
            ],
            elevation=4,
        )
        root_layout.add_widget(toolbar)
        
        self.quote_label = MDLabel(
            text="[color=#3CB371]Yükleniyor...[/color]",
            halign="center", font_style="Caption", italic=True,
            markup=True, adaptive_height=True, padding_y="15dp"
        )
        root_layout.add_widget(self.quote_label)

        float_wrapper = MDFloatLayout()

        content_cluster = MDBoxLayout(
            orientation='vertical', adaptive_height=True, spacing="15dp",
            size_hint_x=0.9, pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.days_label = MDLabel(
            text="--", halign="center", font_style="H2", bold=True,
            padding=[0, 0, 0, "30dp"]
        )
        
        days_text_layout = MDBoxLayout(
            orientation='horizontal', adaptive_height=True, size_hint_x=None,
            width="250dp", spacing="5dp", pos_hint={'center_x': 0.5}
        )
        days_text_label = MDLabel(
            text="Gündür İçmiyorsun", font_style="H6",
            theme_text_color="Secondary", halign="right",
            size_hint_x=None, width="220dp"
        )
        days_text_icon = MDIcon(
            icon="rocket-launch-outline",
            theme_text_color="Secondary", halign="left"
        )
        days_text_layout.add_widget(days_text_label)
        days_text_layout.add_widget(days_text_icon)
        
        self.money_saved_label = MDLabel(text="Biriktirilen Para: ₺--", halign="center", font_style="Body1")
        self.cigarettes_not_smoked_label = MDLabel(text="İçilmeyen Sigara: -- adet", halign="center", font_style="Body1")
        self.life_regained_label = MDLabel(text="Kazanılan Süre: --", halign="center", font_style="Body1")

        content_cluster.add_widget(self.days_label)
        content_cluster.add_widget(days_text_layout)
        content_cluster.add_widget(MDLabel(size_hint_y=None, height="15dp"))
        content_cluster.add_widget(self.money_saved_label)
        content_cluster.add_widget(self.cigarettes_not_smoked_label)
        content_cluster.add_widget(self.life_regained_label)
        content_cluster.add_widget(MDLabel(size_hint_y=None, height="15dp"))
        
        self.milestone_card = MDCard(
            orientation="vertical", padding="12dp", spacing="8dp",
            size_hint_y=None, height="140dp"
        )
        self.milestone_title = MDLabel(text="Sağlık Gelişimi", font_style="H6", size_hint_y=None, height="32dp")
        self.see_all_button = MDTextButton(text="Tüm Başarıları Gör", pos_hint={'center_x': 0.5}, on_release=lambda x: self.go_to_achievements())
        self.milestone_last_achieved_label = MDLabel(text="Son başarı: Yükleniyor...", font_style="Caption", adaptive_height=True)
        self.milestone_next_label = MDLabel(text="Sonraki hedef: Yükleniyor...", font_style="Body2", adaptive_height=True)
        self.milestone_progress = MDProgressBar(value=0)
        self.milestone_card.add_widget(self.milestone_title)
        self.milestone_card.add_widget(self.see_all_button)
        self.milestone_card.add_widget(self.milestone_last_achieved_label)
        self.milestone_card.add_widget(self.milestone_next_label)
        self.milestone_card.add_widget(self.milestone_progress)
        
        content_cluster.add_widget(self.milestone_card)
        float_wrapper.add_widget(content_cluster)

        panic_button = MDFillRoundFlatButton(
            text="KRİZ ANI", icon="shield-alert-outline",
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            on_release=lambda x: self.show_panic_dialog()
        )
        float_wrapper.add_widget(panic_button)
        
        root_layout.add_widget(float_wrapper)
        self.add_widget(root_layout)
    
    def open_daily_log_dialog(self):
        today_str = datetime.now().strftime('%Y-%m-%d')
        app = MDApp.get_running_app()
        if app.db_manager.check_daily_log_exists(today_str):
            snackbar = MDSnackbar()
            snackbar.text = "Bugün için giriş zaten yapıldı!"
            snackbar.open()
            return
        if not self.daily_log_dialog:
            self.dialog_textfield = MDTextField(hint_text="Bugün içilen sigara adedi", input_filter="int")
            self.daily_log_dialog = MDDialog(
                title="Günlük Sigara Girişi", type="custom",
                content_cls=self.dialog_textfield,
                buttons=[
                    MDFlatButton(text="İPTAL", on_release=lambda x: self.daily_log_dialog.dismiss()),
                    MDFlatButton(text="KAYDET", on_release=self.save_daily_log),
                ],
            )
        self.dialog_textfield.text = ""
        self.daily_log_dialog.open()

    def save_daily_log(self, *args):
        count = self.dialog_textfield.text
        if not count or not count.isdigit():
            snackbar = MDSnackbar()
            snackbar.text = "Lütfen geçerli bir sayı girin."
            snackbar.open()
            return
        today_str = datetime.now().strftime('%Y-%m-%d')
        app = MDApp.get_running_app()
        app.db_manager.add_daily_log(today_str, int(count))
        snackbar = MDSnackbar()
        snackbar.text = "Günün verisi başarıyla kaydedildi."
        snackbar.open()
        self.daily_log_dialog.dismiss()
    
    def show_panic_dialog(self):
        app = MDApp.get_running_app()
        now_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        app.db_manager.log_craving_event(now_timestamp)
        profile_data = app.db_manager.load_user_profile()
        reason_text = "Mücadeleye devam et, başarabilirsin!"
        if profile_data and profile_data[4]:
            personal_reasons = [reason.strip() for reason in profile_data[4].split('\n') if reason.strip()]
            if personal_reasons:
                reason_text = f"Unutma:\n\n'{random.choice(personal_reasons)}'"
        if not self.panic_dialog:
            self.panic_dialog = MDDialog(
                title="Sakin Ol ve Hatırla!", text=reason_text,
                buttons=[
                    MDFlatButton(
                        text="KAPAT", theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.panic_dialog.dismiss()
                    ),
                ],
            )
        self.panic_dialog.text = reason_text
        self.panic_dialog.open()

    def go_to_settings(self):
        self.manager.current = 'settings'

    def go_to_achievements(self):
        self.manager.current = 'achievements'

    def go_to_symptoms(self):
        self.manager.current = 'symptoms'
        
    def go_to_craving_log(self):
        self.manager.current = 'craving_log'

    def go_to_daily_log_history(self):
        self.manager.current = 'daily_log_history'

    def on_enter(self):
        app = MDApp.get_running_app()
        profile_data = app.db_manager.load_user_profile()

        display_pool = list(MOTIVATIONAL_QUOTES)
        if profile_data and profile_data[4]:
            personal_reasons_text = profile_data[4]
            user_reasons = [reason.strip() for reason in personal_reasons_text.split('\n') if reason.strip()]
            if user_reasons:
                display_pool.extend(user_reasons * 3)
        quote = random.choice(display_pool)
        self.quote_label.text = f"[color=#3CB371]\"{quote}\"[/color]"
        
        if profile_data:
            self.milestone_card.opacity = 1
            quit_date, cigs_per_day, price_per_pack, _, personal_reasons = profile_data
            
            last_smoked_date_str = app.db_manager.get_last_smoked_date()
            
            # DÜZELTME: Değişken adı 'quit_date_str' yerine 'quit_date' olmalı
            streak_start_date_str = quit_date
            if last_smoked_date_str:
                last_smoked_date = datetime.strptime(last_smoked_date_str, '%Y-%m-%d')
                streak_start_date_str = (last_smoked_date + timedelta(days=1)).strftime('%Y-%m-%d')

            streak_start_date = datetime.strptime(streak_start_date_str, '%Y-%m-%d')
            smoke_free_days = (datetime.now() - streak_start_date).days
            self.days_label.text = str(smoke_free_days) if smoke_free_days >= 0 else "0"

            tracker = QuitTracker(quit_date, cigs_per_day, price_per_pack)
            
            money = tracker.calculate_money_saved()
            cigs_not_smoked = tracker.calculate_cigarettes_not_smoked()
            life_regained = tracker.calculate_life_regained()

            self.money_saved_label.text = f"Biriktirilen Para: ₺{money:.2f}"
            self.cigarettes_not_smoked_label.text = f"İçilmeyen Sigara: {cigs_not_smoked} adet"
            self.life_regained_label.text = f"Kazanılan Süre: {life_regained}"

            milestone_status = tracker.get_milestone_status()
            last_achieved = milestone_status.get("last_achieved")
            next_milestone = milestone_status.get("next")

            if last_achieved:
                self.milestone_last_achieved_label.text = f"Son başarı: {last_achieved}"
            else:
                self.milestone_last_achieved_label.text = "İlk hedefinize doğru ilerliyorsunuz!"

            if next_milestone:
                self.milestone_next_label.text = f"Sonraki: {next_milestone['description']}"
                hours_needed = next_milestone['hours_needed']
                achieved_count = len(milestone_status['achieved'])
                previous_milestone_hours = tracker.HEALTH_MILESTONES[achieved_count-1][0] if achieved_count > 0 else 0
                total_hours_for_next = hours_needed - previous_milestone_hours
                hours_progressed = tracker.total_hours_smoke_free - previous_milestone_hours
                progress_percentage = (hours_progressed / total_hours_for_next) * 100 if total_hours_for_next > 0 else 100
                self.milestone_progress.value = progress_percentage
            else:
                self.milestone_next_label.text = "Tebrikler! Tüm hedeflere ulaştınız!"
                self.milestone_progress.value = 100
        else:
            self.days_label.text = "!"
            self.days_text_label.text = "Lütfen Ayarlar'dan bilgilerinizi girin."
            self.money_saved_label.text = ""
            self.cigarettes_not_smoked_label.text = ""
            self.life_regained_label.text = ""
            self.milestone_card.opacity = 0