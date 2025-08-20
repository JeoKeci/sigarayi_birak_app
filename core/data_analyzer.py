# core/data_analyzer.py

from datetime import datetime
from collections import Counter

# Türkçe gün isimleri için bir liste (datetime.weekday() 0=Pazartesi, 6=Pazar döner)
TURKISH_DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

class DataAnalyzer:
    def __init__(self, timestamp_logs):
        """
        Analizciyi başlatır.
        :param timestamp_logs: Veritabanından gelen zaman damgası listesi.
                               (Örn: [('2025-08-20 18:00:00',), ('2025-08-19 18:05:00',)])
        """
        self.datetimes = []
        for log in timestamp_logs:
            try:
                # Zaman damgası string'ini datetime nesnesine çevir
                self.datetimes.append(datetime.strptime(log[0], '%Y-%m-%d %H:%M:%S'))
            except (ValueError, TypeError):
                continue # Hatalı formatı görmezden gel

    def find_most_frequent_day(self):
        """
        En çok kriz yaşanan günü bulur.
        """
        if not self.datetimes:
            return "Veri Yok"
        
        # Her bir tarihin haftanın hangi gününe denk geldiğini bul (0-6)
        weekdays = [d.weekday() for d in self.datetimes]
        # En sık tekrar eden günü bul
        most_common_day_index = Counter(weekdays).most_common(1)[0][0]
        
        return TURKISH_DAYS[most_common_day_index]

    def find_most_frequent_time_slot(self):
        """
        En çok kriz yaşanan saat dilimini bulur.
        """
        if not self.datetimes:
            return "Veri Yok"
            
        slots = {
            "Sabah (06-12)": 0,
            "Öğleden Sonra (12-17)": 0,
            "Akşam (17-22)": 0,
            "Gece (22-06)": 0
        }
        
        for d in self.datetimes:
            hour = d.hour
            if 6 <= hour < 12:
                slots["Sabah (06-12)"] += 1
            elif 12 <= hour < 17:
                slots["Öğleden Sonra (12-17)"] += 1
            elif 17 <= hour < 22:
                slots["Akşam (17-22)"] += 1
            else:
                slots["Gece (22-06)"] += 1
        
        # En yüksek değere sahip olan zaman dilimini bul
        # (Eğer hepsi 0 ise None döner, bu durumu kontrol edelim)
        max_slot = max(slots, key=slots.get)
        if slots[max_slot] == 0:
            return "Veri Yok"

        return max_slot