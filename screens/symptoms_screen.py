# screens/symptoms_screen.py

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
# DEĞİŞİKLİK: ThreeLineListItem yerine MDLabel kullanacağız
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from core.symptoms_data import WITHDRAWAL_SYMPTOMS


class SymptomsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root_layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(
            title="Yoksunluk Belirtileri ve İpuçları",
            left_action_items=[["arrow-left", lambda x: self.go_back()]],
            elevation=4,
        )
        root_layout.add_widget(toolbar)

        scroll = MDScrollView()
        
        self.symptom_list = MDList()
        scroll.add_widget(self.symptom_list)
        
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)

    def go_back(self):
        self.manager.current = 'home'

    def on_enter(self):
        """
        Ekran her açıldığında, belirtileri ve ipuçlarını listeye ekle.
        """
        if not self.symptom_list.children:
            for symptom_data in WITHDRAWAL_SYMPTOMS:
                
                # --- DEĞİŞİKLİK: İçerik için esnek bir Boxlayout ve Label'lar kullanıyoruz ---
                content_box = MDBoxLayout(
                    orientation="vertical",
                    adaptive_height=True,
                    spacing="8dp",
                    padding=("16dp", "0dp", "16dp", "8dp") # Kenar boşlukları
                )

                timing_label = MDLabel(
                    # markup=True, metin içinde [b] (kalın) gibi etiketler kullanmamızı sağlar
                    text=f"[b]Zamanlama:[/b]\n{symptom_data['timing']}",
                    adaptive_height=True,
                    markup=True 
                )
                tips_label = MDLabel(
                    text=f"[b]İpuçları:[/b]\n{symptom_data['tips']}",
                    adaptive_height=True,
                    markup=True
                )

                content_box.add_widget(timing_label)
                content_box.add_widget(tips_label)
                # --------------------------------------------------------------------------

                panel = MDExpansionPanel(
                    content=content_box, # İçerik olarak yeni kutumuzu atıyoruz
                    panel_cls=MDExpansionPanelOneLine(
                        text=symptom_data['symptom'],
                    )
                )
                self.symptom_list.add_widget(panel)