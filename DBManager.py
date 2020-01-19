import sqlite3
from sqlite3 import OperationalError
from typing import List
from Media import Media
from TagTableManager import TagTableManager
from MediaTableManager import MediaTableManager


class DatabaseManager:

    def __init__(self, database_name: str):
        self.__conn = sqlite3.connect(database_name)
        self.__cursor = self.__conn.cursor()
        self.__media_manager = MediaTableManager(self.__conn, self.__cursor)
        self.__tag_manager = TagTableManager(self.__conn, self.__cursor)

    def create_database(self):
        try:
            self.__media_manager.create_table()
            self.__tag_manager.create_table()
            self.__conn.commit()
        except OperationalError:
            raise RuntimeError("Database exists")

    def write_database_changes(self):
        self.__conn.commit()

    def initialize_database(self, media_list: List[Media]):
        for media in media_list:
            self.add_media(media)

    def add_media(self, media: Media):
        self.__media_manager.add_media(media)
        self.__tag_manager.add_media(media)

    def get_all_media(self) -> List[Media]:
        media_list = []
        for media in self.__media_manager.get_all_media():
            media.tags = self.__tag_manager.get_media_tags(media)
            media_list.append(media)
        return media_list
