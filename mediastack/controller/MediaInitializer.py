import os
import sqlalchemy as sa
from typing import List, Dict
from mediastack.model.Media import Media
from mediastack.model.Category import Category
from mediastack.model.Artist import Artist
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag
from mediastack.utility.Thumbnailer import Thumbnailer
from mediastack.utility.MediaIO import MediaIO

class MediaInitializer:
    def __init__(self, session: sa.orm.Session, media_dir: str = "media/", thumbnail_dir: str = "thumbs/"):
        self._session = session
        self.media_directory = media_dir
        self.thumbnail_directory = thumbnail_dir

        self._mediaio = MediaIO()
        self._thumbnailer = Thumbnailer(self.thumbnail_directory)

    def initialize_media_from_disk(self):
        #print("Scanning disk...")
        media_paths = MediaIO.scan_directory(self.media_directory)
        #print("Disabling missing Media...")
        self._disable_missing_media(media_paths)
        #print("Initializing new Media on Disk...")
        self._intialize_new_media(media_paths)

        self._session.commit()

    def _disable_missing_media(self, media_paths):
        missing_media = 0
        for media in self._session.query(Media).all():
            if (media.path not in media_paths):
                missing_media += 1
                media.path = None
        #print(str(missing_media) + " missing media found.")

    def _intialize_new_media(self, media_paths: List[str]):
        new_media = self._find_new_media(media_paths)
        #print(str(len(new_media)) + " new media found.")
        for media_file_path in new_media:
            #print("Initializing: " + media_file_path)
            media_hash = MediaIO.hash_file(media_file_path)
            media = self._session.query(Media).filter(Media.hash == media_hash).first()
            if media is None:
                media = self._initialize_media(media_file_path)
                if media is not None:
                    self._session.add(media)
            elif media.path != None and os.path.isfile(media.path):
                #print("WARNING DUPLICATE FILE: " + media_file_path)
                continue
            else:
                media.path = media_file_path
                if media.artist_name is not None:
                    media.artist.media.remove(media)
                if media.album_name is not None:
                    media.album.media.remove(media)
                if media.category_name is not None:
                    media.category.media.remove(media)
                self._initialize_media_references(media, self._mediaio.extract_metadata_from_media_file(media_file_path))

    def _find_new_media(self, media_paths: List[str]):
        new_media = []
        for media_file_path in media_paths:
            if not self._session.query(sa.exists().where(Media.path == media_file_path)).scalar():
                new_media.append(media_file_path)
        return new_media

    def _initialize_media(self, media_path: str) -> Media:
        media_metadata = self._mediaio.extract_metadata_from_media_file(media_path)

        if media_metadata is None:
            #print("Couldn't initialize: " + media_path)
            return None

        media = Media()
        
        media.path = media_path
        media.type = media_metadata["type"]
        media.hash = media_metadata["hash"]
        media.source = media_metadata["source"]
        media.score = media_metadata["score"]

        if not self._thumbnailer.create_thumbnail(media_path):
            #print("Failed to thumbnail: " + media_path)
            return None

        self._initialize_media_references(media, media_metadata)

        for tag_name in media_metadata["tags"]:
            current_tag = self._generate_model(tag_name, Tag)
            self._session.add(current_tag)
            media.tags.append(current_tag)
            if media.album is not None and current_tag not in media.album.tags:
                media.album.tags.append(current_tag)
            
        return media

    def _initialize_media_references(self, media: Media, media_metadata: Dict):

        media_category = self._generate_model(media_metadata["category"], Category)
        if (media_category is not None):
            self._session.add(media_category)
            media_category.media.append(media)
        
        media_artist = self._generate_model(media_metadata["artist"], Artist)
        if (media_artist is not None):
            self._session.add(media_artist)
            media_artist.media.append(media)
        
        media_album = self._generate_model(media_metadata["album"], Album)
        if (media_album is not None):
            self._session.add(media_album)
            media_album.media.append(media)

    def _generate_model(self, name: str, model_class):
        if (name is None):
            return None
        model = self._session.query(model_class).filter(model_class.name == name).first()
        if (model is None):
            return model_class(name)
        return model
