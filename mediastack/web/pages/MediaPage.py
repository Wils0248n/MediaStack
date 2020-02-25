from web.pages.BaseWebPage import BaseWebPage
from typing import List, Dict
from html_writer import Html
from controller.MediaManager import MediaManager

class MediaPage(BaseWebPage):
    def __init__(self, media_manager: MediaManager):
        super(MediaPage, self).__init__(media_manager)

    def generate_page(self, request: Dict) -> str:
        queries = request["queries"]
        if "hash" in queries:
            self._media = self._media_manager.find_media(queries["hash"][0])
        elif "index" in queries:
            self._current_index = int(queries["index"][0])
            self._album_name = queries["name"][0]
            self._album = self._media_manager.get_album_media(self._album_name)
            self._media = self._album[self._current_index]
        else:
            return None
        
        self._generate_media_page_media(request)
        self._generate_media_info_sidebar(request)
        if "index" in queries:
            self._generate_footer()
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def _generate_media_page_media(self, request: Dict):
        with self.body.tag('div', id_="media"):
            if "index" in request["queries"]:
                next_index = self._current_index + 1 if self._current_index + 1 < len(self._album) else 0
                href = "/album?name=" + str(self._media.album) + "&index=" + str(next_index)
            else:
                href = self._media.path
            with self.body.tag('a', attributes=dict(href=href)):
                self._generate_media(self._media)

    def _generate_media_info_sidebar(self, request: Dict):
        with self.body.tag('div', id_="media_info"):
            with self.body.tag('p') as label:
                label += "Type:"
                if self._media.type is not None:
                    self.body.tag_with_content(self._media.type, 'a', attributes=dict(href="/media?search=type:" + self._media.type))
            with self.body.tag('p') as label:
                label += "Category:"
                if self._media.category is not None:
                    self.body.tag_with_content(str(self._media.category), 'a', attributes=dict(href="/media?search=category:" + str(self._media.category)))
            with self.body.tag('p') as label:
                label += "Artist:"
                if self._media.artist is not None:
                    self.body.tag_with_content(str(self._media.artist), 'a', attributes=dict(href="/media?search=artist:" + str(self._media.artist)))
            #with self.body.tag('p', classes=["meta_count"]) as artist_count:
                #artist_count += "(" + str(self._media_manager.count_media_with_artist(self._media.artist)) + ")"
            with self.body.tag('p') as label:
                label += "Album:"
                if self._media.album is not None:
                    self.body.tag_with_content(str(self._media.album), 'a', attributes=dict(href="/album?name=" + str(self._media.album)))
            with self.body.tag('p') as label:
                label += "Source:"
                if self._media.source is not None:
                    self.body.tag_with_content("source website", 'a', attributes=dict(href=self._media.source))

            self.body.tag_with_content("Tags:", 'p')
            with self.body.tag('ul', attributes=dict(style="list-style-type:none;")):
                for tag in self._media.tags:
                    with self.body.tag('li'):
                        self.body.tag_with_content(str(tag), 'a', attributes=dict(href="/?search=" + str(tag)))
                        self.body.tag_with_content(" (" + str(self._media_manager.count_media_with_tag(tag.name)) + ")", 'p')

            with self.body.tag('div', id_='"add_tag"'):
                with self.body.tag('form', attributes=dict(action="", method="post")):
                    self.body.self_close_tag('input', attributes=dict(type="text",
                                                                        placeholder="Tag Name", name="add_tag"))
                    self.body.tag_with_content("Add Tag", 'button', attributes=dict(type="submit", text="Add Tag"))

    def _generate_footer(self):
        next_index = self._current_index + 1 if self._current_index + 1 < len(self._album) else 0
        prev_index = self._current_index - 1 if not self._current_index == 0 else len(self._album) - 1
        with self.body.tag('div', id_="album_footer"):
            with self.body.tag('p') as current_page_label:
                self.body.tag_with_content("<<", 'a',
                                             attributes=dict(href="/album?name" + str(self._media.album) + "&index=" + str(prev_index)))
                current_page_label += str(self._current_index + 1) + " / " + str(len(self._album))
                self.body.tag_with_content(">>", 'a',
                                             attributes=dict(href="/album?name=" + str(self._media.album) + "&index=" + str(next_index)))

    def _generate_media(self, media):
        if media.type == "image" or media.type == "animated_image":
            self.body.self_close_tag('img', id_="image", attributes=dict(src="/" + media.path))
        elif media.type == "video":
            with self.body.tag('video', id_="video", attributes=dict(controls=True, autoplay=True, muted=True)):
                self.body.self_close_tag('source', attributes=dict(src="/" + media.path, type="video/mp4"))