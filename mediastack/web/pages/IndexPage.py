from typing import Dict
from html_writer import Html
from web.pages.BaseWebPage import BaseWebPage
from controller.MediaManager import MediaManager

class IndexPage(BaseWebPage):
    def __init__(self, media_manager: MediaManager):
        super(IndexPage, self).__init__(media_manager)

    def generate_page(self, request: Dict) -> str:
        self.generate_search_form(request)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)
