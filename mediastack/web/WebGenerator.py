from html_writer import Html
from typing import List, Dict
from web.pages import *
from controller.MediaManager import MediaManager
from utility.MediaUtility import read_file_bytes

class WebGenerator:
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def generate_page(self, request: Dict):
        if "hash" in request["queries"] or "index" in request["queries"]:
            return MediaPage(self._media_manager).generate_page(request)
        if request["page"] == "/media" or request["page"] == "/album" or request["page"] == "/all" or "search" in request["queries"]:
            return ThumbnailPage(self._media_manager).generate_page(request)
        if request["page"] == "/":
            return IndexPage(self._media_manager).generate_page(request)
        else:
            return "404"
