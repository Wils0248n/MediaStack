import os
from typing import List, Dict
from model.Base import Base
from model.Media import Media
from model.Tag import Tag
from model.Album import Album
from model.Relations import media_tag_table
from controller.SearchManager import SearchManager
from sqlalchemy import create_engine, select, exists
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from utility.Thumbnailer import Thumbnailer
from utility.MediaUtility import *


class MediaManager:

    def __init__(self, media_directory: str, thumbnail_directory: str):
        if not os.path.isdir(media_directory):
            raise ValueError("Invalid Media Directory.")
        self.media_directory = media_directory
        self.thumbnail_directory = thumbnail_directory
        self._search_manager = SearchManager()
        self._thumbnailer = Thumbnailer(thumbnail_directory)
        
        self._engine = create_engine('sqlite:////media/Projects/MediaStack/test.db')
        Base.metadata.create_all(bind=self._engine)
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()
    
        self._initialize_media_from_disk()

    def _initialize_media_from_disk(self):
        for media_file_path in self._get_new_media():
            print(media_file_path)
            media = self.find_media(hash_file(media_file_path))
            if media is None:
                self._session.add(self._initialize_media(media_file_path))
            else:
                meta = extract_media_meta(media_file_path)
                media.path = media_file_path
                media.category = meta["category"]
                media.artist = meta["artist"]
                media.album = meta["album"]

        self._session.commit()
    
    def _get_new_media(self):
        new_media = []
        for media_file_path in scan_directory(self.media_directory):
            if not self._session.query(exists().where(Media.path == media_file_path)).scalar():
                new_media.append(media_file_path)
        return new_media

    def _initialize_media(self, media_path: str) -> Media:
        meta = extract_media_meta(media_path)
        media = Media()
        media_hash = hash_file(media_path)
        media.hash = media_hash
        media.path = media_path
        media.category = meta["category"]
        media.artist = meta["artist"]
        media.album = meta["album"]
        media.source = extract_source(media_path)
        media.type = determine_media_type(media_path)
        media.score = 0
        self._thumbnailer.create_thumbnail(media)
        for tag in extract_keywords(media_path):
            current_tag = self.find_tag(tag)
            if current_tag is None:
                current_tag = self._initialize_tag(tag)
                self._session.add(current_tag)
            media.tags.append(current_tag)
        if meta["album"] is not None:
            album = self.find_album(meta["album"])
            if album is None:
                album = self._initialize_album(meta["album"], media_hash)
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

    def find_media(self, media_hash: str) -> Media:
        return self._session.query(Media).get(media_hash)

    def find_tag(self, tag_name: str) -> Tag:
        return self._session.query(Tag).get(tag_name)

    def find_album(self, album_name: str) -> Album:
        return self._session.query(Album).get(album_name)

    def count_media_with_tag(self, tag_name: str) -> int:
        return self._session.execute(
            self._session.query(media_tag_table)
            .filter_by(tags=tag_name)
            .statement.with_only_columns([func.count()])
            .order_by(None)
        ).scalar()

    def count_media_with_artist(self, artist_name: str) -> int:
        return self._session.execute(
            self._session.query(Media)
            .filter_by(artist=artist_name)
            .statement.with_only_columns([func.count()])
            .order_by(None)
        ).scalar()

    def search(self, criteria: List[str]) -> List[Media]:
        search_result = self._search_manager.search(self.get_media(), criteria)
        search_result.sort()
        return search_result

    def search_all(self, criteria: List[str]) -> List[Media]:
        search_result = self._search_manager.search(self.get_all_media(), criteria)
        search_result.sort()
        return search_result

    def get_album_media(self, album_name: str) -> List[Media]:
        album_media_list = list(self._session.query(Media).filter(Media.album == album_name.lower()))
        album_media_list.sort()
        return album_media_list

    def get_media(self) -> List[Media]:
        media_list = list(self._session.query(Media).filter(Media.album == None))
        for album in self._session.query(Album).all():
            media_list.append(self.find_media(album.cover))
        media_list.sort()
        return media_list

    def get_all_media(self) -> List[Media]:
        return self._session.query(Media).all()

    def get_media_album_index(self, media_hash: str) -> int:
        media = self.find_media(media_hash)
        album_list = self.get_album_media(media.album)
        album_list.sort()
        return album_list.index(media)
