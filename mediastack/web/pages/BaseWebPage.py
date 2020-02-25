from abc import ABC
from html_writer import Html
from typing import Dict
from controller.MediaManager import MediaManager

class BaseWebPage(ABC):
    def __init__(self, media_manager: MediaManager):
        self.head = Html()
        self.body = Html()
        self._media_manager = media_manager
        self._generate_header()
        self._generate_nav()

    def _generate_header(self):
        self.head.self_close_tag('meta', attributes=dict(charset='utf-8'))
        self.head.tag_with_content("MediaStack", name='title')
        self.head.self_close_tag('link', attributes=dict(href="/style.css", rel="stylesheet", type="text/css"))

    def _generate_nav(self):
        header_tag_type = 'h4'
        with self.body.tag('div', id_='"header"'):
            with self.body.tag('a',  attributes=dict(href="/media")):
                self.body.tag_with_content("Media", header_tag_type)
            self.body.tag_with_content(" | ", header_tag_type)
            with self.body.tag('a',  attributes=dict(href="/")):
                self.body.tag_with_content("Index", header_tag_type)
            self.body.tag_with_content(" | ", header_tag_type)
            with self.body.tag('a',  attributes=dict(href="/all")):
                self.body.tag_with_content("All", header_tag_type)

    def generate_search_form(self, request: Dict):
        queries = request["queries"]
        previous_search = "" if "search" not in queries else ' '.join([str(query) for query in queries["search"]])
        with self.body.tag('div', id_='"search"'):
            with self.body.tag('form', attributes=dict(action="media", method="get")):
                self.body.self_close_tag('input', attributes=dict(type="text", value=str(previous_search),
                                                                    placeholder="search...", name="search"))
                self.body.tag_with_content("Search", 'button', attributes=dict(type="submit", text="search"))
