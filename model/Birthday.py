import sqlite3
from typing import List, Optional

import config

conn = sqlite3.connect(config.DB_NAME)

MONTH_LENGTHS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Birthday:
    def __init__(self, user_id: int, name: str, day: int, month: int):
        self.user_id = user_id
        self.name = name
        self.day = day
        self.month = month

    @staticmethod
    def save(user_id: int, name: str, day: int, month: int):
        cursor = None
        try:
            sql = "INSERT INTO birthdays(`user_id`, `name`, `day`, `month`) VALUES(?,?,?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, name, day, month))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def delete(user_id: int, name: str):
        cursor = None
        try:
            sql = "DELETE FROM birthdays WHERE `user_id` = ? AND `name` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, name))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getByUserIdAndName(user_id: int, name: str) -> Optional["Birthday"]:
        cursor = None
        try:
            sql = "SELECT * FROM birthdays WHERE `user_id` = ? AND `name` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, name))
            result = cursor.fetchone()
            if not result:
                return None
            return Birthday(result[4], result[3], result[1], result[2])
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getByUserId(user_id: int) -> List["Birthday"]:
        cursor = None
        try:
            sql = "SELECT * FROM birthdays WHERE `user_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            results = cursor.fetchall()
            return [
                Birthday(result[4], result[3], result[1], result[2])
                for result in results
            ]
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getAll() -> List["Birthday"]:
        cursor = None
        try:
            sql = "SELECT * FROM birthdays"
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            return [
                Birthday(result[4], result[3], result[1], result[2])
                for result in results
            ]
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def init():
        try:
            cursor = conn.cursor()
            sql = """
                CREATE TABLE IF NOT EXISTS birthdays (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    day INTEGER CHECK(day >= 1 AND day <= 31),
                    month INTEGER CHECK(month >= 1 AND month <= 12),
                    name TEXT NOT NULL,
                    user_id BIGINT NOT NULL,
                    UNIQUE(name, user_id)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Birthday\n{e}")
            exit()
