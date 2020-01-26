import os
from typing import List, Dict
from Media import Media, hash_file
from Album import Album
from SearchManager import SearchManager
from DBManager import DatabaseManager
from Thumbnailer import Thumbnailer


class MediaManager:

    def __init__(self, media_directory: str, thumbnail_directory: str):
        if not os.path.isdir(media_directory):
            raise ValueError("Invalid Media Directory.")
        self.__media_directory = media_directory
        self.__thumbnail_directory = thumbnail_directory
        self.__media_list: List[Media] = []
        self.__albums: Dict[str, Album] = {}
        self.__db_manager = DatabaseManager("test.db")
        self.__thumbnailer = Thumbnailer(thumbnail_directory)
        self.__initialize_media()

    def __initialize_media(self):
        try:
            self.__db_manager.create_database()
            print("Initializing Media...")
            self.__initialize_media_from_disk()
            print("Done. Added " + str(len(self.__media_list)) + " Media.\nAdding Media to DB...")
            self.__db_manager.add_media_from_list(self.__media_list)
            print("Done.")
        except RuntimeError:
            print("Database exists...\nInitializing from DB...")
            self.__initialize_media_from_database()
            print("Done.\nVerifying Media Files...")
            self.__verify_database()
            print("Done, Initialized " + str(len(self.__media_list)) + " Media.")
        print("Initializing Albums...")
        self.__initialize_albums()
        print("Done.\nCreating Thumbnails...")
        self.__create_thumbnails()
        print("Done.")

    def __initialize_media_from_database(self):
        for media in self.__db_manager.get_all_media():
            self.__media_list.append(media)

    def __initialize_media_from_disk(self):
        for media_file_path in self.__scan_media_directory():
            try:
                media = Media(media_file_path)
                self.__media_list.append(media)
            except ValueError as e:
                print(str(e))

    def __scan_media_directory(self) -> List[str]:
        media_file_paths = []
        for currentDirectory, directories, files in os.walk(self.__media_directory):
            for file in files:
                media_file_paths.append(os.path.join(currentDirectory, file))
        return media_file_paths

    def __initialize_albums(self):
        for media in self.__media_list:
            if media.album is not None:
                self.__add_media_to_albums(media)

    def __add_media_to_albums(self, media: Media):
        if media.album not in self.__albums.keys():
            self.__albums[media.album] = Album(media)
        else:
            self.__albums[media.album].add_media(media)

    def __create_thumbnails(self):
        for media in self.__media_list:
            self.__thumbnailer.create_thumbnail(media)

    def find_media(self, media_hash: str) -> Media:
        for media in self.__media_list:
            if media.hash == media_hash:
                return media

    def get_albums(self) -> Dict[str, Album]:
        for album in self.__albums.values():
            album.media_list.sort()
        return self.__albums

    def get_media(self) -> List[Media]:
        media_list = []
        for media in self.__media_list:
            if media.album is None:
                media_list.append(media)

        for album in self.__albums.values():
            album.media_list.sort()
            media_list.append(album.get_cover())

        media_list.sort()
        return media_list

    def update_media_tags(self, media: Media):
        self.__db_manager.update_media_tags(media)

    def get_all_media(self) -> List[Media]:
        self.__media_list.sort()
        return self.__media_list

    def search(self, search_query: List[str]) -> List[Media]:
        media_list = SearchManager().search(self.get_media(), search_query)
        media_list.sort()
        return media_list

    def search_all(self, search_query: List[str]) -> List[Media]:
        media_list = SearchManager().search(self.__media_list, search_query)
        media_list.sort()
        return media_list

    def get_media_tags_statistics(self, media: Media) -> Dict[str, int]:
        return self.__db_manager.get_tags_statistics(media.tags)

    def __verify_database(self):
        new_media = self.__get_new_media()
        self.__db_manager.verify_database(new_media)
        for media in new_media:
            self.__media_list.append(media)

    def __get_new_media(self) -> List[Media]:
        new_media = []
        current_media_paths = [media.path for media in self.__media_list]
        for media_path in self.__scan_media_directory():
            if media_path not in current_media_paths:
                new_media.append(Media(media_path))
        return new_media


if __name__ == '__main__':
    MediaManager("media/", "thumbs/")
