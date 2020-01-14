import sqlite3
from sqlite3 import OperationalError

class databaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        self.createDataBase()

    def createDataBase(self):
        try:
            self.cursor.execute("""CREATE TABLE imagedata (
                hash text,
                filename text,
                category text,
                artist text,
                album text,
                tags text
            )""")
            self.conn.commit()
        except OperationalError:
            pass

    def addImageToDB(self, hash, filename, category, artist, album, tags):
        self.cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?)", (hash, filename, category, artist, album, tags))
        self.conn.commit()
