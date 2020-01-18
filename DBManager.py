import sqlite3
from sqlite3 import OperationalError
from sqlite3.dbapi2 import Cursor
from TagTableManager import TagTableManager
from MediaTableManager import MediaTableManager


class DatabaseManager:
    cursor: Cursor

    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        self.media_manager = MediaTableManager(self.conn, self.cursor)
        self.tag_manager = TagTableManager(self.conn, self.cursor)

    def create_database(self):
        try:
            self.media_manager.create_table()
            self.tag_manager.create_table()
            self.conn.commit()
        except OperationalError:
            raise RuntimeError("Database exists")

    def write_database_changes(self):
        self.conn.commit()

    def initialize_database(self, media_list):
        for media in media_list:
            self.add_media(media)

    def add_media(self, media):
        self.media_manager.add_media(media)
        self.tag_manager.add_media(media)

    def get_all_media(self):
        media_list = []
        for media in self.media_manager.get_all_media():
            media.tags = self.tag_manager.get_media_tags(media)
            media_list.append(media)
        return media_list

if __name__ == '__main__':
    dbm = DatabaseManager()
    print(dbm.search_database([]))
    dbm.conn.close()