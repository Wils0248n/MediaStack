import os
from typing import Tuple, Dict
from urllib import parse
from utility.MediaUtility import read_file_bytes
from web.WebGenerator import WebGenerator
from controller.MediaManager import MediaManager

class RequestHandler:

    def __init__(self):
        self._media_directory = "media/"
        self._thumbnail_directory = "thumbs/"
        self._media_manager = MediaManager(self._media_directory, self._thumbnail_directory)
        self._web_generator = WebGenerator(self._media_manager)
        self._encoding = "UTF-8"

    def handle_get_request(self, request: Dict) -> Tuple[str, bytes]:
        print("GET:")
        print(request)
        if request["page"] == "/style.css":
            return 'text/css', read_file_bytes("/style.css")
        if request["page"].startswith("/" + self._media_directory) or request["page"].startswith("/" + self._thumbnail_directory):
            return '', read_file_bytes(parse.unquote(request["page"]))
        return 'text/html', bytes(self._web_generator.generate_page(request), self._encoding)
        
    def handle_post_request(self, request: Dict) -> Tuple[str, bytes]:
        print("POST:")
        print(request)

        return 'text/html', bytes(self._web_generator.generate_page(request), self._encoding)
