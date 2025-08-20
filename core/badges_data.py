# core/badges_data.py

# Kazanılabilecek rozetlerin tanımlandığı liste.
# Her bir rozet bir sözlük (dictionary) olarak tanımlanır.

BADGES_DATA = [
    # Gün bazlı rozetler
    {
        "id": "days_1",
        "name": "İlk Adım",
        "description": "Sigarasız ilk 24 saatini tamamladın!",
        "icon": "badge_days_1.png",
        "condition_type": "days",
        "condition_value": 1,
    },
    {
        "id": "days_3",
        "name": "Zorlu 72 Saat",
        "description": "Nikotinin vücudundan tamamen atıldığı ilk 3 günü başardın!",
        "icon": "badge_days_3.png",
        "condition_type": "days",
        "condition_value": 3,
    },
    {
        "id": "days_7",
        "name": "Bir Haftalık Şampiyon",
        "description": "Tebrikler, sigarasız bir haftayı geride bıraktın!",
        "icon": "badge_days_7.png",
        "condition_type": "days",
        "condition_value": 7,
    },
    # Para bazlı rozetler
    {
        "id": "money_100",
        "name": "Kumbaram Doluyor",
        "description": "Sigaraya harcamayarak 100 TL biriktirdin!",
        "icon": "badge_money_1.png",
        "condition_type": "money",
        "condition_value": 100,
    },
    {
        "id": "money_500",
        "name": "Akıllı Yatırımcı",
        "description": "Tasarrufların 500 TL'ye ulaştı, harika gidiyorsun!",
        "icon": "badge_money_2.png",
        "condition_type": "money",
        "condition_value": 500,
    },
    # İçilmeyen sigara bazlı rozetler
    {
        "id": "cigs_100",
        "name": "100'ler Kulübü",
        "description": "Tam 100 adet sigarayı içmeyi reddettin!",
        "icon": "badge_cigs_1.png",
        "condition_type": "cigs",
        "condition_value": 100,
    },
    {
        "id": "cigs_500",
        "name": "500'ü Devirdin",
        "description": "İçmediğin sigara sayısı 500'e ulaştı!",
        "icon": "badge_cigs_2.png",
        "condition_type": "cigs",
        "condition_value": 500,
    },
]