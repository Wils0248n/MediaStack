from abc import ABC
from html_writer import Html
from typing import List, Dict
from model.Media import Media
from model.Album import Album
from model.MediaType import MediaType

class BaseWebPage(ABC):
    def __init__(self, thumbnail_directory: str):
        self.thumbnail_directory = thumbnail_directory
        self.head = Html()
        self.body = Html()
        self.__generate_header()
        self.__generate_nav()

    def __generate_header(self):
        self.head.self_close_tag('meta', attributes=dict(charset='utf-8'))
        self.head.tag_with_content("MediaStack", name='title')
        self.head.self_close_tag('link', attributes=dict(href="/style.css", rel="stylesheet", type="text/css"))

    def __generate_nav(self):
        header_tag_type = 'h4'
        with self.body.tag('div', id_='"header"'):
            with self.body.tag('a',  attributes=dict(href="/?search=")):
                self.body.tag_with_content("Media", header_tag_type)
            self.body.tag_with_content(" | ", header_tag_type)
            with self.body.tag('a',  attributes=dict(href="/")):
                self.body.tag_with_content("Index", header_tag_type)
            self.body.tag_with_content(" | ", header_tag_type)
            with self.body.tag('a',  attributes=dict(href="/all")):
                self.body.tag_with_content("All", header_tag_type)

    def generate_search_form(self, previous_search):
        with self.body.tag('div', id_='"search"'):
            with self.body.tag('form', attributes=dict(action="")):
                self.body.self_close_tag('input', attributes=dict(type="text", value=previous_search,
                                                                    placeholder="search...", name="search"))
                self.body.tag_with_content("Search", 'button', attributes=dict(type="submit", text="search"))

    def generate_thumbnails(self, media_list: List[Media]):
        with self.body.tag('div', id_='"thumbnails"'):
            for media in media_list:
                if media.album is None:
                    href = "media=" + media.hash
                else:
                    href = "album=" + str(media.album) + "/" + str(media.album.get_index(media))
                with self.body.tag('a', attributes=dict(href=href)):
                    self.body.self_close_tag('img', classes=["thumbnail", "media_thumbnail"], 
                        attributes=dict(src=self.thumbnail_directory + media.hash))

    def generate_media(self, media: Media):
        if media.type == MediaType.IMAGE or media.type == MediaType.ANIMATED_IMAGE:
            self.body.self_close_tag('img', id_="image", attributes=dict(src="/" + media.path))
        elif media.type == MediaType.VIDEO:
            with self.body.tag('video', id_="video", attributes=dict(controls=True, autoplay=True, muted=True)):
                self.body.self_close_tag('source', attributes=dict(src="/" + media.path, type="video/mp4"))
