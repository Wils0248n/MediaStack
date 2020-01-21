from html_writer import Html
from typing import List, Dict
from Media import Media
from Album import Album


class WebGenerator:
    def __init__(self, thumbnail_directory: str):
        self.__head = Html()
        self.__body = Html()
        self.__thumbnail_directory = thumbnail_directory

    def __generate_html_header(self):
        self.__head.self_close_tag('meta', attributes=dict(charset='utf-8'))
        self.__head.tag_with_content("Photo Stack Testing...", name='title')
        self.__head.self_close_tag('link', attributes=dict(href="/style.css", rel="stylesheet", type="text/css"))

    def generate_index(self, media_list: List[Media], previous_search: str = "") -> str:
        self.__head = Html()
        self.__body = Html()
        self.__generate_html_header()
        self.__generate_body_header()
        self.__generate_index_search_form(previous_search)
        self.__generate_index_thumbnails(media_list)
        return Html.html_template(self.__head, self.__body).to_raw_html(indent_size=2)

    def generate_all_page(self, media_list: List[Media], album_dict: Dict[str, Album]) -> str:
        self.__head = Html()
        self.__body = Html()
        self.__generate_html_header()
        self.__generate_body_header()
        self.__generate_search_thumbnails(media_list, album_dict)
        return Html.html_template(self.__head, self.__body).to_raw_html(indent_size=2)

    def __generate_body_header(self):
        with self.__body.tag('div', id_='"header"'):
            self.__body.tag_with_content("Header Here", 'p')

    def __generate_index_search_form(self, previous_search):
        with self.__body.tag('div', id_='"search"'):
            with self.__body.tag('form', attributes=dict(action="")):
                self.__body.self_close_tag('input', attributes=dict(type="text", value=previous_search,
                                                                    placeholder="search...", name="search"))
                self.__body.tag_with_content("Search", 'button', attributes=dict(type="submit", text="search"))

    def __generate_index_thumbnails(self, media_list: List[Media]):
        with self.__body.tag('div', id_='"thumbnails"'):
            for media in media_list:
                if media.album is None:
                    with self.__body.tag('a', attributes=dict(href="media=" + media.hash)):
                        self.__body.self_close_tag('img', classes=["thumbnail", "media_thumbnail"],
                                                   attributes=dict(src=self.__thumbnail_directory + media.hash))
                else:
                    with self.__body.tag('a', attributes=dict(href="album=" + media.album + "/0")):
                        self.__body.self_close_tag('img', classes=["thumbnail", "album_thumbnail"],
                                                   attributes=dict(src=self.__thumbnail_directory + media.hash))

    def __generate_search_thumbnails(self, media_list: List[Media], album_dict: Dict[str, Album]):
        with self.__body.tag('div', id_='"thumbnails"'):
            for media in media_list:
                if media.album is None:
                    with self.__body.tag('a', attributes=dict(href="media=" + media.hash)):
                        self.__body.self_close_tag('img', classes=["thumbnail", "media_thumbnail"],
                                                   attributes=dict(src=self.__thumbnail_directory + media.hash))
                else:
                    media_album_index = album_dict[media.album].media_list.index(media)
                    with self.__body.tag('a', attributes=dict(href="album=" + media.album + "/" + str(media_album_index))):
                        self.__body.self_close_tag('img', classes=["thumbnail", "album_thumbnail"],
                                                   attributes=dict(src=self.__thumbnail_directory + media.hash))

    def generate_media_page(self, media: Media) -> str:
        self.__head = Html()
        self.__body = Html()
        self.__generate_body_header()
        self.__generate_html_header()
        self.__generate_media_page_media(media)
        self.__generate_media_info_sidebar(media)
        return Html.html_template(self.__head, self.__body).to_raw_html(indent_size=2)

    def __generate_media_info_sidebar(self, media: Media):
        with self.__body.tag('div', id_="media_info"):
            with self.__body.tag('p') as label:
                label += "Type:"
                if media.type is not None:
                    self.__body.tag_with_content(media.type.value, 'a', attributes=dict(href="/?search=type:"
                                                                                        + media.type.value))
            with self.__body.tag('p') as label:
                label += "Category:"
                if media.category is not None:
                    self.__body.tag_with_content(str(media.category), 'a', attributes=dict(href="/?search=category:"
                                                                                            + str(media.category)))
            with self.__body.tag('p') as label:
                label += "Artist:"
                if media.artist is not None:
                    self.__body.tag_with_content(str(media.artist), 'a', attributes=dict(href="/?search=artist:"
                                                                                          + str(media.artist)))
            with self.__body.tag('p') as label:
                label += "Album:"
                if media.album is not None:
                    self.__body.tag_with_content(str(media.album), 'a', attributes=dict(href="/album=" + str(media.album)))
            with self.__body.tag('p') as label:
                label += "Source:"
                if media.source is not None:
                    self.__body.tag_with_content("source website", 'a', attributes=dict(href=media.source))

            self.__body.tag_with_content("Tags:", 'p')
            with self.__body.tag('ul', attributes=dict(style="list-style-type:none;")):
                for tag in media.tags:
                    with self.__body.tag('li'):
                        self.__body.tag_with_content(tag, 'a', attributes=dict(href="/?search=" + tag))

    def __generate_media_page_media(self, media: Media):
        with self.__body.tag('div', id_="media"):
            with self.__body.tag('a', attributes=dict(href=media.path)):
                self.__generate_media_tag(media)

    def __generate_media_tag(self, media: Media):
        if media.type == Media.Type.IMAGE or media.type == Media.Type.ANIMATED_IMAGE:
            self.__body.self_close_tag('img', id_="image", attributes=dict(src="/" + media.path))
        elif media.type == Media.Type.VIDEO:
            with self.__body.tag('video', id_="video", attributes=dict(controls=True)):
                self.__body.self_close_tag('source', attributes=dict(src="/" + media.path, type="video/mp4"))

    def generate_album_page(self, album: Album) -> str:
        self.__head = Html()
        self.__body = Html()
        self.__generate_html_header()
        self.__generate_body_header()
        self.__generate_album_page_thumbnails(album)
        return Html.html_template(self.__head, self.__body).to_raw_html(indent_size=2)

    def __generate_album_page_thumbnails(self, album: Album):
        with self.__body.tag('div', id_='"thumbnails"'):
            for media in album.media_list:
                media_album_index = album.media_list.index(media)
                with self.__body.tag('a', attributes=dict(href="album=" + media.album + "/" + str(media_album_index))):
                    self.__body.self_close_tag('img', classes=["thumbnail", "album_thumbnail"],
                                               attributes=dict(src=self.__thumbnail_directory + media.hash))

    def generate_album_media_page(self, album: Album, current_index: int) -> str:
        self.__head = Html()
        self.__body = Html()
        self.__generate_html_header()
        self.__generate_body_header()
        self.__generate_album_media_page_media(album, current_index)
        self.__generate_media_info_sidebar(album.media_list[current_index])
        self.__generate_album_media_page_footer(album, current_index)
        return Html.html_template(self.__head, self.__body).to_raw_html(indent_size=2)

    def __generate_album_media_page_media(self, album: Album, current_index: int):
        media = album.media_list[current_index]
        next_index = current_index + 1 if current_index + 1 < len(album.media_list) else 0
        with self.__body.tag('div', id_="media"):
            with self.__body.tag('a', attributes=dict(href="/album=" + media.album + "/" + str(next_index))):
                self.__generate_media_tag(media)

    def __generate_album_media_page_footer(self, album: Album, current_index: int):
        pass
