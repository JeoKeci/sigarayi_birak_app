# screens/achievements_screen.py

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget
# YENİ: Grid Layout, Label ve Image bileşenlerini içe aktarıyoruz
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from core.tracker import QuitTracker

class AchievementsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = MDBoxLayout(orientation='vertical')
        toolbar = MDTopAppBar(
            title="Başarılarım",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=4,
        )
        root_layout.add_widget(toolbar)

        # --- YENİ YAPI: Ana kaydırılabilir alan ---
        scroll = MDScrollView()
        # Kaydırılabilir alanın içinde dikey bir layout olacak
        main_content_layout = MDBoxLayout(orientation='vertical', adaptive_height=True, padding="10dp", spacing="20dp")

        # 1. Bölüm: Kazanılan Rozetler
        main_content_layout.add_widget(MDLabel(text="Kazanılan Rozetler", font_style="H5", adaptive_height=True))
        # Rozetleri ızgara (grid) düzeninde göstereceğiz
        self.badge_grid = MDGridLayout(
            cols=3, # Her satırda 3 rozet
            spacing="20dp",
            adaptive_height=True
        )
        main_content_layout.add_widget(self.badge_grid)

        # 2. Bölüm: Sağlık Hedefleri
        main_content_layout.add_widget(MDLabel(text="Ulaşılan Sağlık Hedefleri", font_style="H5", adaptive_height=True))
        self.milestone_list = MDList()
        main_content_layout.add_widget(self.milestone_list)

        scroll.add_widget(main_content_layout)
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)
        # ----------------------------------------

    def go_back(self):
        self.manager.current = 'home'

    def on_enter(self):
        """
        Ekran açıldığında hem rozetleri hem de sağlık hedeflerini yükle.
        """
        self.badge_grid.clear_widgets()
        self.milestone_list.clear_widgets()

        app = MDApp.get_running_app()
        profile_data = app.db_manager.load_user_profile()

        if profile_data:
            quit_date, cigs_per_day, price_per_pack, _, _ = profile_data
            tracker = QuitTracker(quit_date, cigs_per_day, price_per_pack)

            # --- Rozetleri Yükle ---
            unlocked_badges = tracker.get_unlocked_badges()
            if not unlocked_badges:
                self.badge_grid.add_widget(MDLabel(text="Henüz hiç rozet kazanmadın.", adaptive_height=True))
            else:
                for badge in unlocked_badges:
                    # Her bir rozet için dikey bir kutu oluştur
                    badge_box = MDBoxLayout(orientation='vertical', adaptive_height=True, spacing="5dp")
                    badge_box.add_widget(Image(
                        source=f"assets/badges/{badge['icon']}",
                        size_hint_y=None,
                        height="80dp" # İkon yüksekliği
                    ))
                    badge_box.add_widget(MDLabel(
                        text=badge['name'],
                        halign='center',
                        font_style='Caption',
                        adaptive_height=True
                    ))
                    self.badge_grid.add_widget(badge_box)

            # --- Sağlık Hedeflerini Yükle (Milestones) ---
            milestone_status = tracker.get_milestone_status()
            achieved_milestones = milestone_status.get("achieved", [])

            if not achieved_milestones:
                item = TwoLineAvatarIconListItem(
                    text="Henüz bir sağlık hedefine ulaşmadınız.",
                    secondary_text="Yolun başındasınız, devam edin!",
                )
                item.add_widget(ImageLeftWidget(source="assets/icons/rocket-launch-outline.png"))
                self.milestone_list.add_widget(item)
            else:
                for achievement_text in achieved_milestones:
                    item = TwoLineAvatarIconListItem(
                        text="Başarıyla Tamamlandı!",
                        secondary_text=achievement_text,
                        secondary_font_style="Caption",
                    )
                    item.add_widget(ImageLeftWidget(source="assets/icons/check-decagram.png"))
                    self.milestone_list.add_widget(item)