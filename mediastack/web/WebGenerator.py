from html_writer import Html
from typing import List, Dict
from web.pages import *
from model.Media import Media
from model.Album import Album


class WebGenerator:
    def __init__(self, thumbnail_directory: str):
        self.__thumbnail_directory = thumbnail_directory

    def generate_index(self, previous_search: str = "") -> str:
        return IndexPage(self.__thumbnail_directory).generate_page(previous_search)

    def generate_search_page(self, media_list: List[Media], previous_search: str = "") -> str:
        return SearchPage(self.__thumbnail_directory).generate_page(media_list, previous_search)

    def generate_all_page(self, media_list: List[Media], previous_search: str = "") -> str:
        return AllPage(self.__thumbnail_directory).generate_page(media_list, previous_search)

    def generate_media_page(self, media: Media) -> str:
        return MediaPage(self.__thumbnail_directory).generate_page(media)

    def generate_album_page(self, album: Album) -> str:
        return AlbumPage(self.__thumbnail_directory).generate_page(album)

    def generate_album_media_page(self, media: Media, current_index: int) -> str:
        return AlbumMediaPage(self.__thumbnail_directory).generate_page(media, current_index)
