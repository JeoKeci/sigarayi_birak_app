# screens/daily_log_history_screen.py

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from datetime import datetime
import locale

try:
    locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
except locale.Error:
    print("Türkçe locale ayarlanamadı.")

TURKISH_MONTHS = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
TURKISH_DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

class DailyLogHistoryScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.edit_dialog = None
        self.dialog_textfield = None
        self.date_to_edit = None

        root_layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(
            title="Geçmiş Günlük Girişleri",
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
        self.populate_log_list()

    def populate_log_list(self):
        self.log_list.clear_widgets()
        app = MDApp.get_running_app()
        logs = app.db_manager.load_all_daily_logs()

        for log_entry in logs:
            date_str, count = log_entry
            try:
                dt_object = datetime.strptime(date_str, '%Y-%m-%d')
                day = dt_object.day
                month_name = TURKISH_MONTHS[dt_object.month]
                year = dt_object.year
                day_name = TURKISH_DAYS[dt_object.weekday()]
                formatted_date = f"{day} {month_name} {year}, {day_name}"
            except (ValueError, TypeError, IndexError):
                formatted_date = date_str

            item = TwoLineAvatarIconListItem(
                text=formatted_date,
                secondary_text=f"{count} adet sigara içildi",
                on_release=lambda x, log=log_entry: self.open_edit_dialog(log)
            )
            item.add_widget(ImageLeftWidget(source="assets/icons/notebook-edit-outline.png"))
            self.log_list.add_widget(item)

    def open_edit_dialog(self, log_data):
        date_str, current_count = log_data
        self.date_to_edit = date_str

        if not self.edit_dialog:
            self.dialog_textfield = MDTextField(hint_text="Yeni sigara adedi", input_filter="int")
            self.edit_dialog = MDDialog(
                title=f"Girişi Düzenle",
                type="custom",
                content_cls=self.dialog_textfield,
                buttons=[
                    MDFlatButton(text="İPTAL", on_release=lambda x: self.edit_dialog.dismiss()),
                    MDFlatButton(text="GÜNCELLE", on_release=self.save_edited_log),
                ],
            )
        
        self.edit_dialog.title = f"Girişi Düzenle: {date_str}"
        self.dialog_textfield.text = str(current_count)
        self.edit_dialog.open()

    def save_edited_log(self, *args):
        new_count = self.dialog_textfield.text
        if not new_count or not new_count.isdigit():
            snackbar = MDSnackbar()
            snackbar.text = "Lütfen geçerli bir sayı girin."
            snackbar.open()
            return
            
        app = MDApp.get_running_app()
        app.db_manager.update_daily_log(self.date_to_edit, int(new_count))
        
        snackbar = MDSnackbar()
        snackbar.text = "Giriş başarıyla güncellendi."
        snackbar.open()
        
        self.edit_dialog.dismiss()
        self.populate_log_list() # Listeyi yenile