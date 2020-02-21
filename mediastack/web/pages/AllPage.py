from web.pages.BaseWebPage import BaseWebPage
from typing import List, Dict
from html_writer import Html
from model.Media import Media
from model.Album import Album

class AllPage(BaseWebPage):
    def __init__(self, thumbnail_directory: str):
        super(AllPage, self).__init__(thumbnail_directory)

    def generate_page(self, media_list: List[Media], previous_search: str) -> str:
        self.generate_search_form(previous_search)
        self.generate_thumbnails(media_list)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)
