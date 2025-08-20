# screens/craving_log_screen.py

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineIconListItem, ImageLeftWidget
from kivymd.uix.label import MDLabel
# YENİ: Analiz modülümüzü ve Card bileşenini içe aktarıyoruz
from core.data_analyzer import DataAnalyzer
from kivymd.uix.card import MDCard
from datetime import datetime

# Türkçe karakter sorununu çözmek için kendi listelerimiz
TURKISH_MONTHS = [
    "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", 
    "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
]
TURKISH_DAYS = [
    "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"
]

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

        # Ana layout'u kaydırılabilir hale getiriyoruz
        scroll = MDScrollView()
        main_content_layout = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp", spacing="10dp")

        # --- YENİ BÖLÜM: ANALİZ ÖZETİ KARTI ---
        analysis_card = MDCard(
            orientation="vertical",
            padding="15dp",
            spacing="5dp",
            size_hint_y=None,
            height="120dp",
            md_bg_color=(0.2, 0.2, 0.2, 1) # Koyu bir arkaplan
        )
        analysis_card.add_widget(MDLabel(text="Analiz Özeti", font_style="H6", adaptive_height=True))
        self.most_frequent_day_label = MDLabel(text="En zorlu gün: Hesaplanıyor...", adaptive_height=True)
        self.most_frequent_slot_label = MDLabel(text="En zorlu saatler: Hesaplanıyor...", adaptive_height=True)
        
        analysis_card.add_widget(self.most_frequent_day_label)
        analysis_card.add_widget(self.most_frequent_slot_label)
        main_content_layout.add_widget(analysis_card)
        # ----------------------------------------
        
        main_content_layout.add_widget(MDLabel(text="Tüm Kriz Anları", font_style="H6", adaptive_height=True))
        self.log_list = MDList()
        main_content_layout.add_widget(self.log_list)

        scroll.add_widget(main_content_layout)
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)

    def go_back(self):
        self.manager.current = 'home'

    def on_enter(self):
        self.log_list.clear_widgets()

        app = MDApp.get_running_app()
        logs = app.db_manager.load_craving_logs()

        # --- YENİ BÖLÜM: VERİLERİ ANALİZ ETME VE GÖSTERME ---
        analyzer = DataAnalyzer(logs)
        most_frequent_day = analyzer.find_most_frequent_day()
        most_frequent_slot = analyzer.find_most_frequent_time_slot()

        self.most_frequent_day_label.text = f"En zorlu günün: [b]{most_frequent_day}[/b]"
        self.most_frequent_slot_label.text = f"En zorlu saatlerin: [b]{most_frequent_slot}[/b]"
        # Önemli: Yukarıdaki etiketlerde [b]...[/b] kullanabilmek için markup=True ekliyoruz.
        self.most_frequent_day_label.markup = True
        self.most_frequent_slot_label.markup = True
        # ----------------------------------------------------

        if not logs:
            self.log_list.add_widget(
                MDLabel(
                    text="Henüz kaydedilmiş bir kriz anı yok.",
                    halign="center", theme_text_color="Secondary", padding_y="20dp"
                )
            )
            return

        for log_entry in logs:
            timestamp_str = log_entry[0]
            
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

            item = OneLineIconListItem(text=formatted_time)
            icon = ImageLeftWidget(source="assets/icons/history.png")
            item.add_widget(icon)
            self.log_list.add_widget(item)