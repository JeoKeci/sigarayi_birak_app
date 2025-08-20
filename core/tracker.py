# core/tracker.py

from datetime import datetime
from .health_data import HEALTH_MILESTONES
# YENİ: Bir önceki adımda oluşturduğumuz rozet verilerini içe aktarıyoruz.
from .badges_data import BADGES_DATA

class QuitTracker:
    def __init__(self, quit_date_str, cigarettes_per_day, price_per_pack):
        self.quit_date = datetime.strptime(quit_date_str, '%Y-%m-%d')
        self.cigarettes_per_day = cigarettes_per_day
        self.price_per_pack = price_per_pack
        self.cigarettes_in_pack = 20
        self.HEALTH_MILESTONES = HEALTH_MILESTONES
        self.delta = datetime.now() - self.quit_date
        self.total_hours_smoke_free = self.delta.total_seconds() / 3600

    def calculate_days_smoke_free(self):
        return self.delta.days

    def calculate_money_saved(self):
        days_smoke_free = self.calculate_days_smoke_free()
        if days_smoke_free < 0: return 0
        daily_cost = (self.cigarettes_per_day / self.cigarettes_in_pack) * self.price_per_pack
        return days_smoke_free * daily_cost

    def calculate_cigarettes_not_smoked(self):
        days_smoke_free = self.calculate_days_smoke_free()
        if days_smoke_free < 0: return 0
        return days_smoke_free * self.cigarettes_per_day

    def calculate_life_regained(self):
        cigs_not_smoked = self.calculate_cigarettes_not_smoked()
        if cigs_not_smoked <= 0: return "0 gün"
        minutes_regained = cigs_not_smoked * 11
        days = int(minutes_regained // (60 * 24))
        remaining_minutes = minutes_regained % (60 * 24)
        hours = int(remaining_minutes // 60)
        if days > 0: return f"{days} gün, {hours} saat"
        else: return f"{hours} saat"

    def get_milestone_status(self):
        achieved_milestones = []
        next_milestone = None
        for hours_needed, description in self.HEALTH_MILESTONES:
            if self.total_hours_smoke_free >= hours_needed:
                achieved_milestones.append(description)
            else:
                next_milestone = {"hours_needed": hours_needed, "description": description}
                break
        return {
            "achieved": achieved_milestones,
            "last_achieved": achieved_milestones[-1] if achieved_milestones else None,
            "next": next_milestone
        }

    # --- YENİ FONKSİYON ---
    def get_unlocked_badges(self):
        """
        Kullanıcının mevcut istatistiklerine göre kilidini açtığı rozetleri belirler.
        """
        unlocked_badges = []
        # Mevcut durumdaki istatistikleri alalım
        current_days = self.calculate_days_smoke_free()
        current_money = self.calculate_money_saved()
        current_cigs = self.calculate_cigarettes_not_smoked()

        # Tüm rozetleri kontrol et
        for badge in BADGES_DATA:
            unlocked = False
            condition_type = badge["condition_type"]
            condition_value = badge["condition_value"]

            # Koşul türüne göre kontrol yap
            if condition_type == "days" and current_days >= condition_value:
                unlocked = True
            elif condition_type == "money" and current_money >= condition_value:
                unlocked = True
            elif condition_type == "cigs" and current_cigs >= condition_value:
                unlocked = True
            
            # Eğer rozetin kilidi açıldıysa, listeye ekle
            if unlocked:
                unlocked_badges.append(badge)
        
        return unlocked_badges