import sqlite3
import os

class USER_DATA:
    def __init__(self, db_path='User_Data.db'):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS User_Data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    _name TEXT,
                    _sur_name TEXT,
                    _patronymic TEXT,
                    _access_level INTEGER
                )
            ''')
            conn.commit()

    def add_user(self, name, sur_name, patronymic, access_level):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO User_Data (_name, _sur_name, _patronymic, _access_level)
                VALUES (?, ?, ?, ?)
            ''', (name, sur_name, patronymic, access_level))
            conn.commit()
            return cursor.lastrowid

    def delete_user_by_name(self, name, sur_name, patronymic):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM User_Data
                WHERE _name = ? AND _sur_name = ? AND _patronymic = ?
            ''', (name, sur_name, patronymic))
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count

    def update_access_level(self, name, sur_name, patronymic, new_access_level):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE User_Data
                SET _access_level = ?
                WHERE _name = ? AND _sur_name = ? AND _patronymic = ?
            ''', (new_access_level, name, sur_name, patronymic))
            updated_count = cursor.rowcount
            conn.commit()
            return updated_count

    def get_size(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM User_Data')
            count = cursor.fetchone()[0]
            return count

    def get_user_by_id(self, id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT _name, _sur_name, _patronymic, _access_level FROM User_Data WHERE id = ?', (id,))
            user = cursor.fetchone()
            if user:
                full_name = f"{user[1]} {user[2]} {user[0]}"
                access_level = user[3]
                return f"{full_name} {access_level}"
            return ""
