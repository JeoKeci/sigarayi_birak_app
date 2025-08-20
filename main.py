# main.py

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from screens.home_screen import HomeScreen
from screens.settings_screen import SettingsScreen
from screens.achievements_screen import AchievementsScreen
from screens.symptoms_screen import SymptomsScreen
# YENİ: Kriz günlüğü ekranını içe aktarıyoruz
from screens.craving_log_screen import CravingLogScreen
from database.db_manager import DatabaseManager 

class SigarayiBirakApp(MDApp):
    
    def change_theme(self, theme_style):
        self.theme_cls.theme_style = theme_style

    def build(self):
        self.db_manager = DatabaseManager()

        profile_data = self.db_manager.load_user_profile()
        if profile_data:
            self.theme_cls.theme_style = profile_data[3]
        else:
            self.theme_cls.theme_style = "Dark"

        self.theme_cls.primary_palette = "Blue"
        self.title = "Sigarayı Bırakma Yardımcın"
        
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(AchievementsScreen(name='achievements'))
        sm.add_widget(SymptomsScreen(name='symptoms'))
        # YENİ: Kriz günlüğü ekranını screen manager'a ekliyoruz
        sm.add_widget(CravingLogScreen(name='craving_log'))
        
        if profile_data is None:
            sm.current = 'settings'
        else:
            sm.current = 'home'

        return sm

if __name__ == "__main__":
    SigarayiBirakApp().run()