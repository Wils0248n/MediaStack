import sqlalchemy as sa
from mediastack.model.Media import Media
from mediastack.model.Media import Tag
from mediastack.model.Media import Album
from mediastack.utility.Thumbnailer import Thumbnailer
from mediastack.utility.MediaUtility import *

class MediaInitializer:
    def __init__(self, session: sa.orm.Session):
        self.media_directory = "media/"
        self.thumbnail_directory = "thumbs/"
        self._thumbnailer = Thumbnailer(thumbnail_directory)
        self._session = session

    def _get_new_media(self):
        new_media = []
        for media_file_path in scan_directory(self.media_directory):
            if not self._session.query(sa.exists().where(Media.path == media_file_path)).scalar():
                new_media.append(media_file_path)
        return new_media

    def initialize_media_from_disk(self):
        print("Initializing Media from Disk...")
        new_media = self._get_new_media()
        print(str(len(new_media)) + " new media found.")
        for media_file_path in new_media:
            print("Initializing: " + media_file_path)
            media = self._session.query(Media).filter(Media.path == media_file_path).first()
            if media is None:
                self._session.add(self._initialize_media(media_file_path))
            else:
                meta = extract_media_meta(media_file_path)
                media.path = media_file_path
                media.category = meta["category"]
                media.artist = meta["artist"]
                media.album_name = meta["album"]
        self._fix_media_album_indexes()

        self._session.commit()

    def _initialize_media(self, media_path: str) -> Media:
        media = Media(media_path)
        for tag in extract_keywords(media_path):
            current_tag = self.find_tag(tag)
            if current_tag is None:
                current_tag = self._initialize_tag(tag)
                self._session.add(current_tag)
            media.tags.append(current_tag)
        if media.album is not None:
            album = self.find_album(media.album)
            if album is None:
                album = self._initialize_album(media.album_name, media.hash)
                self._session.add(album)
            else:
                current_cover = self.find_media(album.cover)
                if current_cover > media:
                    album.cover = hash
        return media

    def _initialize_tag(self, tag_name: str) -> Tag:
        tag = Tag()
        tag.name = tag_name
        return tag

    def _initialize_album(self, album_name: str, og_media_hash: str) -> Album:
        album = Album()
        album.name = album_name
        album.cover = og_media_hash
        return album

    def _fix_media_album_indexes(self):
        for album in self._session.query(Album).all():
            album_media = self.find_all_album_media(album.name)
            album_media.sort()
            for media in album_media:
                media.album_index = album_media.index(media)