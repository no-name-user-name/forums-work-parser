import random
import sqlite3
import string
import time


class DataBase:
    def __init__(self, db_name: str = 'db'):
        self.mydb = sqlite3.connect(f'{db_name}.sqlite')
        self.mydb.row_factory = self.dict_factory
        self.__create_tables()

    @staticmethod
    def dict_factory(cursor, row):
        """Convert cortage to dict"""
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def __create_tables(self):
        cursor = self.mydb.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS urls (
                         id INTEGER PRIMARY KEY,
                         url BIGINT,
                         reg_data DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S','now', 'localtime'))) """)
        cursor.close()

    def add_new_url(self, url: str):
        cursor = self.mydb.cursor()
        cursor.execute("""INSERT INTO urls (url) VALUES (?)""", (url, ))
        self.mydb.commit()
        result = cursor.lastrowid
        cursor.close()
        return result

    def is_new_url(self, url: str):
        cursor = self.mydb.cursor()
        cursor.execute("SELECT * FROM urls WHERE url = ?", (url,))
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            self.add_new_url(url)
            return True
        else:
            return False
