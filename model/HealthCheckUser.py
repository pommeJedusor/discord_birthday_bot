import os
import sqlite3
from typing import List

from dotenv import load_dotenv

load_dotenv()
DATABASE = os.getenv("DATABASE")
if DATABASE is None:
    print("Please set a DATABASE name")
    exit()

conn = sqlite3.connect(DATABASE)


class HealthCheckUser:
    def __init__(self, id: int, purpose: str):
        self.id = id
        self.purpose = purpose

    @staticmethod
    def add(id: int, purpose: str):
        cursor = None
        try:
            sql = "INSERT INTO health_check_users(`health_check_user_id`, `health_check_user_prupose`) VALUES(?,?)"
            cursor = conn.cursor()
            cursor.execute(sql, (id, purpose))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def delete(id: int, purpose: str):
        cursor = None
        try:
            sql = "DELETE FROM health_check_users WHERE `health_check_user_id` = ? AND `health_check_user_purpose` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (id, purpose))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getByPurpose(purpose: str) -> List["HealthCheckUser"]:
        cursor = None
        try:
            sql = "SELECT health_check_user_id, health_check_user_purpose FROM health_check_users WHERE `health_check_user_purpose` = ?"
            cursor = conn.cursor()
            cursor.execute(sql, (purpose, ))
            results = cursor.fetchall()
            return [HealthCheckUser(result[0], result[1]) for result in results]
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def getAll() -> List["HealthCheckUser"]:
        cursor = None
        try:
            sql = "SELECT health_check_user_id, health_check_user_purpose FROM health_check_users"
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            return [HealthCheckUser(result[0], result[1]) for result in results]
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
                CREATE TABLE IF NOT EXISTS health_check_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    health_check_user_id INTEGER NOT NULL,
                    health_check_user_purpose TEXT NOT NULL, 
                    UNIQUE(health_check_user_id, health_check_user_purpose)
                );
            """
            cursor.execute(sql)

            conn.commit()
        except Exception as e:
            print(f"failed to init the sqlite table HealthCheckUsers\n{e}")
            exit()
