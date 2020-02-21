from web.pages.BaseWebPage import BaseWebPage
from html_writer import Html
from model.Album import Album

class AlbumPage(BaseWebPage):
    def __init__(self, thumbnail_directory: str):
        super(AlbumPage, self).__init__(thumbnail_directory)

    def generate_page(self, album: Album) -> str:
        self.generate_album_page_thumbnails(album)
        return Html.html_template(self.head, self.body).to_raw_html(indent_size=2)

    def generate_album_page_thumbnails(self, album: Album):
        with self.body.tag('div', id_='"thumbnails"'):
            for media in album.media_list:
                media_album_index = album.media_list.index(media)
                with self.body.tag('a', attributes=dict(href="album=" + str(media.album) + "/" + str(media_album_index))):
                    self.body.self_close_tag('img', classes=["thumbnail", "album_thumbnail"],
                                               attributes=dict(src=self.thumbnail_directory + media.hash))
