import os
from typing import List, Dict
from mediastack.model.Base import Base
from mediastack.model.Media import Media
from mediastack.model.Tag import Tag
from mediastack.model.Album import Album
from mediastack.controller.SearchManager import SearchManager
from mediastack.controller.MediaInitializer import MediaInitializer
from sqlalchemy import create_engine, select, exists
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func


class MediaManager:

    def __init__(self):
        self._engine = create_engine('sqlite:////media/Projects/MediaStack/test.db', connect_args={'check_same_thread': False})
        Base.metadata.create_all(bind=self._engine)
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()
    
        self._media_initializer = MediaInitializer(self._session)
        self._media_initializer.initialize_media_from_disk();

        self._search_manager = SearchManager()

    def find_media(self, media_hash: str) -> Media:
        return self._session.query(Media).get(media_hash)

    def find_media_by_album(self, album_name: str, album_index: int):
        return self._session.query(Media).filter(Media.album == album_name, Media.album_index == album_index).first()

    def find_tag(self, tag_name: str) -> Tag:
        return self._session.query(Tag).get(tag_name)

    def find_album(self, album_name: str) -> Album:
        return self._session.query(Album).get(album_name)

    def find_all_album_media(self, album_name: str) -> List[Media]:
        album_media_list = list(self._session.query(Media).filter(Media.album == album_name.lower()))
        album_media_list.sort()
        return album_media_list

    def search(self, criteria: List[str]) -> List[Media]:
        search_result = self._search_manager.search(self.get_media(), criteria)
        search_result.sort()
        return search_result

    def search_all(self, criteria: List[str]) -> List[Media]:
        search_result = self._search_manager.search(self.get_all_media(), criteria)
        search_result.sort()
        return search_result

    def get_media(self) -> List[Media]:
        media_list = list(self._session.query(Media).filter(Media.album == None))
        for album in self._session.query(Album).all():
            media_list.append(album.cover)
        media_list.sort()
        return media_list

    def get_all_media(self) -> List[Media]:
        return self._session.query(Media).all()
