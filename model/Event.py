import os
import sqlite3
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE")
if DATABASE is None:
    print("Please set a DATABASE name")
    exit()

conn = sqlite3.connect(DATABASE)

MONTH_LENGTHS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Event:
    def __init__(self, user_id: int, name: str, minute: int, hour: int, day: int, month: int, year: int):
        self.user_id = user_id
        self.name = name
        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def save(user_id: int, name: str, minute: int, hour: int, day: int, month: int, year: int):
        cursor = None
        try:
            sql = "INSERT INTO events(`user_id`, `name`, `minute`, `hour`, `day`, `month`, `year`) VALUES(?,?,?,?,?,?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, name, minute, hour, day, month, year))
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
            sql = "DELETE FROM events WHERE `user_id` = ? AND `name` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, name))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getByUserIdAndName(user_id: int, name: str) -> Optional["Event"]:
        cursor = None
        try:
            sql = "SELECT * FROM events WHERE `user_id` = ? AND `name` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, name))
            result = cursor.fetchone()
            if not result:
                return None
            return Event(result[7], result[6], result[1], result[2], result[3], result[4], result[5])
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getByUserId(user_id: int) -> List["Event"]:
        cursor = None
        try:
            sql = "SELECT * FROM events WHERE `user_id` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            results = cursor.fetchall()
            return [
                Event(result[7], result[6], result[1], result[2], result[3], result[4], result[5])
                for result in results
            ]
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getByDate(minute: int, hour: int, day: int, month: int, year: int) -> List["Event"]:
        cursor = None
        try:
            sql = "SELECT * FROM events WHERE `minute` = ? AND `hour` = ? AND `day` = ? AND `month` = ? AND `year` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (minute, hour, day, month, year))
            results = cursor.fetchall()
            return [
                Event(result[7], result[6], result[1], result[2], result[3], result[4], result[5])
                for result in results
            ]
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getAll() -> List["Event"]:
        cursor = None
        try:
            sql = "SELECT * FROM events"
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            return [
                Event(result[7], result[6], result[1], result[2], result[3], result[4], result[5])
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
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    minute INTEGER CHECK(minute >= 0 AND minute < 60),
                    hour INTEGER CHECK(hour >= 0 AND hour < 24),
                    day INTEGER CHECK(day >= 1 AND day <= 31),
                    month INTEGER CHECK(month >= 1 AND month <= 12),
                    year YEAR CHECK(YEAR >= 2025),
                    name TEXT NOT NULL,
                    user_id BIGINT NOT NULL,
                    UNIQUE(name, user_id, minute, hour, day, month)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table Event\n{e}")
            exit()
