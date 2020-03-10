import sqlalchemy as sa
from mediastack.model.Media import Media
from mediastack.model.Category import Category
from mediastack.model.Artist import Artist
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag
from mediastack.utility.Thumbnailer import Thumbnailer
from mediastack.utility.MediaUtility import *

class MediaInitializer:
    def __init__(self, session: sa.orm.Session):
        self.media_directory = "media/"
        self.thumbnail_directory = "thumbs/"
        self._thumbnailer = Thumbnailer(self.thumbnail_directory)
        self._session = session

    def initialize_media_from_disk(self):
        print("Scanning disk...")
        media_paths = scan_directory(self.media_directory)
        print("Disabling missing Media...")
        self._disable_missing_media(media_paths)
        print("Initializing new Media on Disk...")
        self._intialize_new_media(media_paths)

        self._session.commit()

    def _disable_missing_media(self, media_paths):
        missing_media = 0
        for media in self._session.query(Media).all():
            if (media.path not in media_paths):
                missing_media += 1
                media.path = None
        print(str(missing_media) + " missing media found.")

    def _intialize_new_media(self, media_paths: List[str]):
        new_media = self._get_new_media(media_paths)
        print(str(len(new_media)) + " new media found.")
        for media_file_path in new_media:
            print("Initializing: " + media_file_path)
            media = self._session.query(Media).filter(Media.hash == hash_file(media_file_path)).first()
            if media is None:
                self._session.add(self._initialize_media(media_file_path))
            else:
                media.path = media_file_path
                media.artist.media.remove(media)
                media.album.media.remove(media)
                media.category.media.remove(media)
                self._initialize_media_references(media)

    def _get_new_media(self, media_paths: List[str]):
        new_media = []
        for media_file_path in media_paths:
            if not self._session.query(sa.exists().where(Media.path == media_file_path)).scalar():
                new_media.append(media_file_path)
        return new_media

    def _initialize_media(self, media_path: str) -> Media:
        media = Media()
        media.hash = hash_file(media_path)
        media.path = media_path
        media.source = extract_source(media_path)
        media.type = determine_media_type(media_path)
        media.score = 0

        self._initialize_media_references(media)

        for tag in extract_keywords(media_path):
            current_tag = self._get_tag(tag)
            self._session.add(current_tag)
            media.tags.append(current_tag)

        self._thumbnailer.create_thumbnail(media)
        return media

    def _initialize_media_references(self, media: Media):
        meta = extract_media_meta(media.path)

        media_category = self._get_category(meta["category"])
        if (media_category is not None):
            self._session.add(media_category)
            media_category.media.append(media)
        
        media_artist = self._get_artist(meta["artist"])
        if (media_artist is not None):
            self._session.add(media_artist)
            media_artist.media.append(media)
        
        media_album = self._get_album(meta["album"])
        if (media_album is not None):
            self._session.add(media_album)
            media_album.media.append(media)

    def _get_tag(self, tag_name: str) -> Tag:
        tag = self._session.query(Tag).filter(Tag.name == tag_name).first()
        if (tag is None):
            return Tag(tag_name)
        return tag

    def _get_category(self, category_name: str) -> Category:
        if (category_name is None):
            return None;
        category = self._session.query(Category).filter(Category.name == category_name).first()
        if (category is None):
            return Category(category_name)
        return category

    def _get_artist(self, artist_name: str) -> Artist:
        if (artist_name is None):
            return None
        artist = self._session.query(Artist).filter(Artist.name == artist_name).first()
        if (artist is None):
            return Artist(artist_name)
        return artist

    def _get_album(self, album_name: str) -> Album:
        if (album_name is None):
            return None
        album = self._session.query(Album).filter(Album.name == album_name).first()
        if (album is None):
            return Album(album_name)
        return album
