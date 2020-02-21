from web.pages.BaseWebPage import BaseWebPage
from typing import List, Dict
from html_writer import Html
from model.Media import Media
from model.Album import Album

class AlbumMediaPage(BaseWebPage):
    def __init__(self, thumbnail_directory: str):
        super(AlbumMediaPage, self).__init__(thumbnail_directory)

    def generate_page(self, media: Media, current_index: int, edit_mode: bool = False) -> str:
        self.generate_album_media_page_media(media, current_index)
        self.generate_media_info_sidebar(media)
        self.generate_album_media_page_footer(media.album, current_index)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def generate_album_media_page_media(self, media: Media, current_index: int):
        next_index = current_index + 1 if current_index + 1 < len(media.album.media_list) else 0
        with self.body.tag('div', id_="media"):
            with self.body.tag('a', attributes=dict(href="/album=" + str(media.album) + "/" + str(next_index))):
                self.generate_media(media)

    def generate_media_info_sidebar(self, media: Media):
        with self.body.tag('div', id_="media_info"):
            with self.body.tag('p') as label:
                label += "Type:"
                if media.type is not None:
                    self.body.tag_with_content(media.type.value, 'a', attributes=dict(href="/?search=type:"
                                                                                        + media.type.value))
            with self.body.tag('p') as label:
                label += "Category:"
                if media.category is not None:
                    self.body.tag_with_content(str(media.category), 'a', attributes=dict(href="/?search=category:"
                                                                                            + str(media.category)))
            with self.body.tag('p') as label:
                label += "Artist:"
                if media.artist is not None:
                    self.body.tag_with_content(str(media.artist), 'a', attributes=dict(href="/?search=artist:"
                                                                                          + str(media.artist)))
            with self.body.tag('p') as label:
                label += "Album:"
                if media.album is not None:
                    self.body.tag_with_content(str(media.album), 'a', attributes=dict(href="/album=" + str(media.album)))
            with self.body.tag('p') as label:
                label += "Source:"
                if media.source is not None:
                    self.body.tag_with_content("source website", 'a', attributes=dict(href=media.source))

            self.body.tag_with_content("Tags:", 'p')
            with self.body.tag('ul', attributes=dict(style="list-style-type:none;")):
                for tag in media.tags:
                    with self.body.tag('li'):
                        self.body.tag_with_content(str(tag), 'a', attributes=dict(href="/?search=" + str(tag)))
                        self.body.tag_with_content(" (" + str(tag.number_of_media) + ")", 'p')

            with self.body.tag('div', id_='"add_tag"'):
                with self.body.tag('form', attributes=dict(action="", method="post")):
                    self.body.self_close_tag('input', attributes=dict(type="text",
                                                                        placeholder="Tag Name", name="add_tag"))
                    self.body.tag_with_content("Add Tag", 'button', attributes=dict(type="submit", text="Add Tag"))

    def generate_album_media_page_footer(self, album: Album, current_index: int):
        media = album.media_list[current_index]
        next_index = current_index + 1 if current_index + 1 < len(album.media_list) else 0
        prev_index = current_index - 1 if not current_index == 0 else len(album.media_list) - 1
        with self.body.tag('div', id_="album_footer"):
            with self.body.tag('p') as current_page_label:
                self.body.tag_with_content("<<", 'a',
                                             attributes=dict(href="/album=" + str(media.album) + "/" + str(prev_index)))
                current_page_label += str(current_index + 1) + " / " + str(len(album.media_list))
                self.body.tag_with_content(">>", 'a',
                                             attributes=dict(href="/album=" + str(media.album) + "/" + str(next_index)))
