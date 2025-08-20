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
            
            # YENİ: Arzulama anlarını kaydetmek için yeni bir tablo
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS cravings_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    craving_timestamp TEXT NOT NULL
                )
            """)
            
            # ... (ALTER TABLE komutları aynı kalıyor) ...
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
        except Exception as e:
            print(f"Profil kaydetme hatası: {e}")
        finally:
            self._close_connection()

    def load_user_profile(self):
        # ... (Bu fonksiyon aynı kalıyor) ...
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
        
    # --- YENİ FONKSİYON ---
    def log_craving_event(self, timestamp):
        """
        Veritabanına yeni bir arzulama (kriz anı) kaydı ekler.
        """
        try:
            self._get_connection()
            self.cursor.execute("INSERT INTO cravings_log (craving_timestamp) VALUES (?)", (timestamp,))
            print(f"Kriz anı günlüğe kaydedildi: {timestamp}")
        except Exception as e:
            print(f"Kriz anı kaydetme hatası: {e}")
        finally:
            self._close_connection()

    def load_craving_logs(self):
        """
        Tüm kriz anı kayıtlarını veritabanından yükler.
        En yeniden en eskiye doğru sıralar.
        """
        logs = []
        try:
            self._get_connection()
            # ORDER BY ... DESC ile en yeni kayıtların en üstte gelmesini sağlıyoruz.
            self.cursor.execute("SELECT craving_timestamp FROM cravings_log ORDER BY craving_timestamp DESC")
            logs = self.cursor.fetchall() # Tüm sonuçları al
        except Exception as e:
            print(f"Kriz günlüğü yükleme hatası: {e}")
        finally:
            self._close_connection()
        return logs