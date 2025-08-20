# database/db_manager.py

import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="user_data.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, '..', db_name)
        self.conn = None
        self.cursor = None
        self.setup_database()

    def _get_connection(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def _close_connection(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def setup_database(self):
        try:
            self._get_connection()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profile (
                    id INTEGER PRIMARY KEY,
                    quit_date TEXT NOT NULL,
                    cigarettes_per_day INTEGER NOT NULL,
                    price_per_pack REAL NOT NULL,
                    theme_style TEXT DEFAULT 'Dark',
                    personal_reasons TEXT DEFAULT ''
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cravings_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    craving_timestamp TEXT NOT NULL
                )
            """)
            
            # Günlük sigara girişlerini tutacak yeni tablo
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_log (
                    log_date TEXT PRIMARY KEY,
                    cigarette_count INTEGER NOT NULL
                )
            """)
            
            try:
                self.cursor.execute("ALTER TABLE user_profile ADD COLUMN theme_style TEXT DEFAULT 'Dark'")
            except sqlite3.OperationalError: pass
            try:
                self.cursor.execute("ALTER TABLE user_profile ADD COLUMN personal_reasons TEXT DEFAULT ''")
            except sqlite3.OperationalError: pass

        except Exception as e:
            print(f"Veritabanı kurulum hatası: {e}")
        finally:
            self._close_connection()
    
    def save_user_profile(self, quit_date, cigarettes_per_day, price_per_pack, theme_style, personal_reasons):
        try:
            self._get_connection()
            self.cursor.execute("""
                INSERT OR REPLACE INTO user_profile (id, quit_date, cigarettes_per_day, price_per_pack, theme_style, personal_reasons)
                VALUES (1, ?, ?, ?, ?, ?)
            """, (quit_date, cigarettes_per_day, price_per_pack, theme_style, personal_reasons))
            print("Kullanıcı profili başarıyla kaydedildi.")
        except Exception as e:
            print(f"Profil kaydetme hatası: {e}")
        finally:
            self._close_connection()

    def load_user_profile(self):
        profile = None
        try:
            self._get_connection()
            self.cursor.execute("SELECT quit_date, cigarettes_per_day, price_per_pack, theme_style, personal_reasons FROM user_profile WHERE id=1")
            profile = self.cursor.fetchone()
        except Exception as e:
            print(f"Profil yükleme hatası: {e}")
        finally:
            self._close_connection()
        return profile
        
    def log_craving_event(self, timestamp):
        try:
            self._get_connection()
            self.cursor.execute("INSERT INTO cravings_log (craving_timestamp) VALUES (?)", (timestamp,))
            print(f"Kriz anı günlüğe kaydedildi: {timestamp}")
        except Exception as e:
            print(f"Kriz anı kaydetme hatası: {e}")
        finally:
            self._close_connection()

    def load_craving_logs(self):
        logs = []
        try:
            self._get_connection()
            self.cursor.execute("SELECT craving_timestamp FROM cravings_log ORDER BY craving_timestamp DESC")
            logs = self.cursor.fetchall()
        except Exception as e:
            print(f"Kriz günlüğü yükleme hatası: {e}")
        finally:
            self._close_connection()
        return logs

    def add_daily_log(self, date_str, count):
        """
        Veritabanına yeni bir günlük sigara kaydı ekler.
        """
        try:
            self._get_connection()
            self.cursor.execute("INSERT INTO daily_log (log_date, cigarette_count) VALUES (?, ?)", (date_str, count))
            print(f"Günlük giriş kaydedildi: {date_str} - {count} adet.")
        except Exception as e:
            print(f"Günlük giriş kaydetme hatası: {e}")
        finally:
            self._close_connection()

    def check_daily_log_exists(self, date_str):
        """
        Belirtilen tarih için bir girişin olup olmadığını kontrol eder.
        """
        log_exists = False
        try:
            self._get_connection()
            self.cursor.execute("SELECT 1 FROM daily_log WHERE log_date = ?", (date_str,))
            if self.cursor.fetchone():
                log_exists = True
        except Exception as e:
            print(f"Günlük giriş kontrol hatası: {e}")
        finally:
            self._close_connection()
        return log_exists
    
    def load_all_daily_logs(self):
        """
        Tüm günlük sigara girişlerini veritabanından yükler.
        En yeniden en eskiye doğru sıralar.
        """
        logs = []
        try:
            self._get_connection()
            self.cursor.execute("SELECT log_date, cigarette_count FROM daily_log ORDER BY log_date DESC")
            logs = self.cursor.fetchall()
        except Exception as e:
            print(f"Geçmiş günlük girişleri yükleme hatası: {e}")
        finally:
            self._close_connection()
        return logs

    def update_daily_log(self, date_str, new_count):
        """
        Belirli bir tarihteki sigara sayısını günceller.
        """
        try:
            self._get_connection()
            self.cursor.execute("UPDATE daily_log SET cigarette_count = ? WHERE log_date = ?", (new_count, date_str))
            print(f"Günlük giriş güncellendi: {date_str} - {new_count} adet.")
        except Exception as e:
            print(f"Günlük giriş güncelleme hatası: {e}")
        finally:
            self._close_connection()
    
     # --- YENİ FONKSİYON ---
    def get_last_smoked_date(self):
        """
        Sigara içildiği girilen en son günü bulur.
        """
        last_date = None
        try:
            self._get_connection()
            # cigarette_count > 0 olan kayıtlar arasından en son tarihi seçiyoruz.
            self.cursor.execute("SELECT MAX(log_date) FROM daily_log WHERE cigarette_count > 0")
            result = self.cursor.fetchone()
            if result and result[0]:
                last_date = result[0]
        except Exception as e:
            print(f"Son sigara içilen günü bulma hatası: {e}")
        finally:
            self._close_connection()
        return last_date