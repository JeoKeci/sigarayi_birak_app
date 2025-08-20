# screens/craving_log_screen.py

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineIconListItem, ImageLeftWidget
from kivymd.uix.label import MDLabel
from datetime import datetime

# --- YENİ BÖLÜM: Türkçe Karakter Sorununu Çözmek İçin Kendi Verilerimiz ---
# Artık işletim sisteminin locale ayarlarına bağımlı değiliz.
TURKISH_MONTHS = [
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", 
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]
TURKISH_DAYS = [
    "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"
]
# -------------------------------------------------------------------------

class CravingLogScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(
            title="Kriz Günlüğüm",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=4,
        )
        root_layout.add_widget(toolbar)

        scroll = MDScrollView()
        
        self.log_list = MDList()
        scroll.add_widget(self.log_list)
        
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)

    def go_back(self):
        self.manager.current = 'home'

    def on_enter(self):
        self.log_list.clear_widgets()

        app = MDApp.get_running_app()
        logs = app.db_manager.load_craving_logs()

        if not logs:
            self.log_list.add_widget(
                MDLabel(
                    text="Henüz kaydedilmiş bir kriz anı yok.",
                    halign="center",
                    theme_text_color="Secondary",
                    padding_y="20dp"
                )
            )
            return

        for log_entry in logs:
            timestamp_str = log_entry[0]
            
            # --- DEĞİŞİKLİK: Tarih ve saati manuel olarak formatlıyoruz ---
            try:
                dt_object = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                
                day = dt_object.day
                month_name = TURKISH_MONTHS[dt_object.month]
                year = dt_object.year
                day_name = TURKISH_DAYS[dt_object.weekday()]
                time_str = dt_object.strftime('%H:%M')

                formatted_time = f"{day} {month_name} {year}, {day_name} - {time_str}"
            except (ValueError, TypeError, IndexError):
                formatted_time = timestamp_str
            # -----------------------------------------------------------

            item = OneLineIconListItem(
                text=formatted_time
            )
            icon = ImageLeftWidget(source="assets/icons/history.png")
            item.add_widget(icon)
            self.log_list.add_widget(item)