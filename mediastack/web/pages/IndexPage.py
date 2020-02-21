from web.pages.BaseWebPage import BaseWebPage
from html_writer import Html

class IndexPage(BaseWebPage):
    def __init__(self, thumbnail_directory: str):
        super(IndexPage, self).__init__(thumbnail_directory)

    def generate_page(self, previous_search: str) -> str:
        self.generate_search_form(previous_search)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)
