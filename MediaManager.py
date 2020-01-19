import os
from typing import List, Dict
from Media import Media
from Album import Album
from SearchManager import SearchManager
from DBManager import DatabaseManager
from Thumbnailer import Thumbnailer


class MediaManager:

    def __init__(self, media_directory: str, thumbnail_directory: str):
        self.__media_directory = media_directory
        self.__thumbnail_directory = thumbnail_directory
        self.__media_list: List[Media] = []
        self.albums: Dict[str, Album] = {}
        self.__db_manager = DatabaseManager("test.db")
        self.__thumbnailer = Thumbnailer(thumbnail_directory)
        self.__initialize()

    def __initialize(self):
        try:
            self.__db_manager.create_database()
            print("Created tables...\nInitializing Media...")
            self.__initialize_media_from_directory(self.__media_directory)
            print("Done.\nAdding Media to DB...")
            self.__add_media_to_database()
            print("Done.")
        except RuntimeError:
            print("Database exists...\nInitializing from DB...")
            self.__initialize_media_from_database()
            print("Done.")
        self.__initialize_albums()

    def __add_media(self, media: Media):
        if media in self.__media_list:
            return
        self.__media_list.append(media)

    def __initialize_media_from_database(self):
        for media in self.__db_manager.get_all_media():
            self.__thumbnailer.create_thumbnail(media)
            self.__add_media(media)

    def __initialize_media_from_directory(self, root_directory: str):
        for currentDirectory, directories, files in os.walk(root_directory):
            for file in files:
                try:
                    media = Media(os.path.join(currentDirectory, file))
                    self.__add_media(media)
                    self.__thumbnailer.create_thumbnail(media)
                except ValueError as e:
                    print(str(e))

    def __add_media_to_database(self):
        for media in self.__media_list:
            self.__db_manager.add_media(media)
        self.__db_manager.write_database_changes()

    def __initialize_albums(self):
        for media in self.__media_list:
            if media.album is not None:
                self.__add_media_to_albums(media)

    def __add_media_to_albums(self, media: Media):
        if media.album not in self.albums.keys():
            self.albums[media.album] = Album(media)
        else:
            self.albums[media.album].add_media(media)

    def find_media(self, media_hash: str) -> Media:
        for media in self.__media_list:
            if media.hash == media_hash:
                return media

    def find_media_album(self, media: Media) -> Album:
        if media.album is None:
            return None
        return self.albums[media.album.name]

    def get_media(self) -> List[Media]:
        media_list = []
        for media in self.__media_list:
            if media.album is None:
                media_list.append(media)

        for album_name in self.albums.keys():
            media_list.append(self.albums[album_name].cover)

        return media_list

    def get_all_media(self) -> List[Media]:
        return self.__media_list

    def search(self, search_query: List[str]) -> List[Media]:
        return SearchManager().search(self.__media_list, search_query)

