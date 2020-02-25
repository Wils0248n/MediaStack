from web.pages.BaseWebPage import BaseWebPage
from html_writer import Html
from typing import Dict
from controller.MediaManager import MediaManager

class ThumbnailPage(BaseWebPage):
    def __init__(self, media_manager: MediaManager):
        super(ThumbnailPage, self).__init__(media_manager)

    def generate_page(self, request: Dict) -> str:
        queries = request["queries"]
        if request["page"] == "/media" or request["page"] == "/":
            if "search" in queries:
                self._media_set = self._media_manager.search(queries["search"])
            else:
                self._media_set = self._media_manager.search([])
        elif request["page"] == "/all":
            if "search" in queries:
                self._media_set = self._media_manager.search_all(queries["search"])
            else:
                self._media_set = self._media_manager.search_all([])
        elif request["page"] == "/album":
            self._media_set = self._media_manager.get_album_media(queries["name"][0])

        self.generate_search_form(request)
        self._generate_thumbnails(request)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def _generate_thumbnails(self, request: Dict):
        with self.body.tag('div', id_='"thumbnails"'):
            for media in self._media_set:
                if media.album is None:
                    href = "media?hash=" + media.hash
                else:
                    href = "album?name=" + str(media.album) + "&index=" + str(self._media_manager.get_media_album_index(media.hash))
                with self.body.tag('a', attributes=dict(href=href)):
                    self.body.self_close_tag('img', classes=["thumbnail", "media_thumbnail"], 
                        attributes=dict(src=self._media_manager.thumbnail_directory + media.hash))