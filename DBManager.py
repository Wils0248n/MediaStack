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

    def initialize_database(self, media_list: List[Media]):
        self.add_media_from_list(media_list)

    def add_media(self, media: Media):
        self.__media_manager.add_media(media)
        self.__tag_manager.add_media(media)
        self.__conn.commit()

    def add_media_from_list(self, media_list: List[Media]):
        for media in media_list:
            self.__media_manager.add_media(media)
            self.__tag_manager.add_media(media)
        self.__conn.commit()

    def get_all_media(self) -> List[Media]:
        media_list = []
        for media in self.__media_manager.get_all_media():
            media.tags = self.__tag_manager.get_media_tags(media)
            media_list.append(media)
        return media_list

    def update_media(self, media: Media):
        self.__media_manager.update_media(media)
        self.__conn.commit()

    def update_media_tags(self, media: Media):
        self.__tag_manager.update_media_tags(media)
        self.__conn.commit()

    def verify_database(self, new_media: List[Media]):
        missing_media_hashes = self.__media_manager.get_missing_media()

        for media in new_media:
            if media.hash in missing_media_hashes:
                print("Updated: " + media.hash)
                self.update_media(media)
                missing_media_hashes.remove(media.hash)
            else:
                print("Added new media: " + media.hash)
                self.add_media(media)

        print("Database missing " + str(len(missing_media_hashes)) + " files.")
