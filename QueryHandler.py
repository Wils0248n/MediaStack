import os
from typing import Tuple
from urllib.parse import unquote
from WebGenerator import WebGenerator
from MediaManager import MediaManager


class QueryHandler:

    def __init__(self):
        self.__media_directory = "media/"
        self.__thumbnail_directory = "thumbs/"
        self.__web_generator = WebGenerator(self.__thumbnail_directory)
        self.__media_manager = MediaManager(self.__media_directory, self.__thumbnail_directory)
        self.__encoding = "UTF-8"

    def handle_get_request(self, request: str) -> Tuple[str, bytes]:
        if request == "/style.css":
            return 'text/css', read_file_bytes("/style.css")
        if request.startswith("/media="):
            return 'text/html', self.__handle_media_request(request)
        if request.startswith("/album="):
            return 'text/html', self.__handle_album_request(request)
        if request.startswith("/" + self.__media_directory) or request.startswith("/" + self.__thumbnail_directory):
            return '', read_file_bytes(unquote(request))
        if request.startswith("/?search="):
            return 'text/html', self.__handle_search_request(request)
        if request == "/all" or request == "/all?search=":
            return 'text/html', self.__handle_all_media_request()
        if request.startswith("/all?search="):
            return 'text/html', self.__handle_search_all_request(request)
        if request == "/":
            return 'text/html', self.__handle_index_request()
        else:
            return '', None

    def __handle_media_request(self, request: str) -> bytes:
        media_hash = request.split('=')[1]
        media = self.__media_manager.find_media(media_hash)
        if media is None:
            return None
        else:
            return bytes(self.__web_generator.generate_media_page(
                media, self.__media_manager.get_media_tags_statistics(media)), self.__encoding)

    def __handle_album_request(self, request: str) -> bytes:
        album_query = request.split('=')[1].split('/')
        album_name = unquote(album_query[0])
        if album_name not in self.__media_manager.get_albums().keys():
            return None
        if len(album_query) == 2:
            current_index = int(request.split('/')[2])
            html_code = self.__web_generator.generate_album_media_page(
                self.__media_manager.get_albums()[album_name],
                current_index,
                self.__media_manager.get_media_tags_statistics(
                    self.__media_manager.get_albums()[album_name].media_list[current_index]))
        elif len(album_query) == 1:
            html_code = self.__web_generator.generate_album_page(self.__media_manager.get_albums()[album_name])
        return bytes(html_code, 'UTF-8')

    def __handle_search_request(self, request: str) -> bytes:
        search_query_list = unquote(request.split('=')[1]).split("+")
        search_query = " ".join(search_query_list)
        search_query_list = [query.lower() for query in search_query_list]
        media = self.__media_manager.search(search_query_list)
        return bytes(self.__web_generator.generate_search_page(media, search_query), self.__encoding)

    def __handle_index_request(self) -> bytes:
        return bytes(self.__web_generator.generate_index(), self.__encoding)

    def __handle_all_media_request(self) -> bytes:
        return bytes(self.__web_generator.generate_all_page(
            self.__media_manager.get_all_media(), self.__media_manager.get_albums()), self.__encoding)

    def __handle_search_all_request(self, request: str) -> bytes:
        search_query_list = unquote(request.split('=')[1]).split("+")
        search_query = " ".join(search_query_list)
        search_query_list = [query.lower() for query in search_query_list]
        media = self.__media_manager.search_all(search_query_list)
        return bytes(self.__web_generator.generate_all_page(
            media, self.__media_manager.get_albums(), search_query), self.__encoding)

    def handle_post_request(self, request: str, post_data: str) -> Tuple[str, bytes]:
        if post_data[0] == "add_tag":
            return 'text/html', self.__handle_add_tag_request(request, post_data)

    def __handle_add_tag_request(self, request, post_data) -> bytes:
        if str.startswith(request, "/media"):
            media = self.__media_manager.find_media(request.split('=')[1])
            media.tags.append(post_data[1])
            self.__media_manager.update_media_tags(media)
            return self.__handle_media_request(request)
        elif str.startswith(request, "/album"):
            album_query = request.split('=')[1].split('/')
            album_name = unquote(album_query[0])
            current_index = int(request.split('/')[2])
            media = self.__media_manager.get_albums()[album_name].media_list[current_index]
            media.tags.append(post_data[1])
            self.__media_manager.update_media_tags(media)
            return self.__handle_album_request(request)


def read_file_bytes(file_path: str) -> bytes:
    try:
        with open(os.getcwd() + file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except IsADirectoryError:
        return None


if __name__ == '__main__':
    QueryHandler()
