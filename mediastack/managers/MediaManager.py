import os
from typing import List, Dict
from model.Media import Media
from model.Album import Album
from model.Artist import Artist
from model.Category import Category
from model.Tag import Tag
from managers.SearchManager import SearchManager
from database.DatabaseManager import DatabaseManager
from utility.Thumbnailer import Thumbnailer
from utility.MediaUtility import scan_directory, extract_media_meta, extract_keywords


class MediaManager:

    def __init__(self, media_directory: str, thumbnail_directory: str):
        if not os.path.isdir(media_directory):
            raise ValueError("Invalid Media Directory.")
        self.__media_directory = media_directory
        self.__thumbnail_directory = thumbnail_directory
        self.__media_list: List[Media] = []
        self.__albums: Dict[str, Album] = {}
        self.__artists: Dict[str, Artist] = {}
        self.__categories: Dict[str, Category] = {}
        self.__tags: Dict[str, Tag] = {}
        self.__search_manager = SearchManager(self.__media_list, self.__categories, self.__artists, self.__albums)
        self.__db_manager = DatabaseManager(":memory:")
        self.__thumbnailer = Thumbnailer(thumbnail_directory)
        self.__initialize_media()

    def __initialize_media(self):
        try:
            #self.__db_manager.create_database()
            print("Initializing Media...")
            self.__initialize_media_from_disk()
            print("Done. Added " + str(len(self.__media_list)) + " Media.\nAdding Media to DB...")
            #self.__db_manager.add_media_from_list(self.__media_list)
            print("Done.")
        except RuntimeError:
            print("Database exists...\nInitializing from DB...")
            self.__initialize_media_from_database()
            print("Done.\nVerifying Media Files...")
            self.__verify_database()
            print("Done, Initialized " + str(len(self.__media_list)) + " Media.")
        print("Done.\nCreating Thumbnails...")
        self.__create_thumbnails()
        print("Done.")

    def __initialize_media_from_database(self):
        for media in self.__db_manager.get_all_media():
            self.__media_list.append(media)

    def __initialize_media_from_disk(self):
        for media_file_path in scan_directory(self.__media_directory):
            try:
                media = Media(media_file_path)
                media_meta = extract_media_meta(media_file_path)
                media.category = self.__initailize_category(media_meta["category"], media)
                media.artist = self.__initailize_artist(media_meta["artist"], media)
                media.album = self.__initalize_album(media_meta["album"], media)
                self.__initailize_media_tags(media)
                self.__media_list.append(media)
            except ValueError as e:
                print(str(e))
        print(self.__media_list[0].tags)
    def __initalize_album(self, album_name: str, media: Media):
        if album_name is None:
            return None
        if album_name not in self.__albums.keys():
            new_album = Album(album_name)
            new_album.add_media(media)
            self.__albums[album_name] = new_album
            return new_album
        else:
            self.__albums[album_name].add_media(media)
            return self.__albums[album_name]

    def __initailize_category(self, category_name: str, media: Media):
        if category_name is None:
            return None
        if category_name not in self.__categories.keys():
            new_category = Category(category_name)
            new_category.add_media(media)
            self.__categories[category_name] = new_category 
            return new_category 
        else:
            self.__categories[category_name].add_media(media)
            return self.__categories[category_name]

    def __initailize_artist(self, artist_name: str, media: Media):
        if artist_name is None:
            return None
        if artist_name not in self.__artists.keys():
            new_artist = Artist(artist_name)
            new_artist.add_media(media)
            self.__artists[artist_name] = new_artist 
            return new_artist 
        else:
            self.__artists[artist_name].add_media(media)
            return self.__artists[artist_name]

    def __initailize_media_tags(self, media: Media):
        keywords = extract_keywords(media.path)
        media_tags = []
        for keyword in keywords:
            if keyword not in self.__tags.keys():
                new_tag = Tag(keyword)
                new_tag.add_media(media)
                self.__tags[keyword] = new_tag
                media_tags.append(new_tag)
            else:
                self.__tags[keyword].add_media(media)
                media_tags.append(self.__tags[keyword])
        media.tags = media_tags

    def __create_thumbnails(self):
        for media in self.__media_list:
            self.__thumbnailer.create_thumbnail(media)

    def find_media(self, media_hash: str) -> Media:
        for media in self.__media_list:
            if media.hash == media_hash:
                return media

    def is_album(self, album_name: str) -> bool:
        return album_name in self.__albums.keys()

    def find_album(self, album_name: str) -> Album:
        return self.__albums[album_name]

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
        media_list = self.__search_manager.search(self.get_media(), search_query)
        media_list.sort()
        return media_list

    def search_all(self, search_query: List[str]) -> List[Media]:
        media_list = self.__search_manager.search(self.__media_list, search_query)
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
        for media_path in scan_directory(self.__media_directory):
            if media_path not in current_media_paths:
                try:
                    new_media.append(Media(media_path))
                except ValueError as e:
                    print(str(e))
        return new_media


if __name__ == '__main__':
    MediaManager("media/", "thumbs/")
