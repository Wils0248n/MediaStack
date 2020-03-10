import sqlalchemy as sa
from enum import Enum
from typing import List
from mediastack.model.Base import Base
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.controller.SearchManager import SearchManager
from mediastack.controller.MediaInitializer import MediaInitializer

import time

class MediaSet(Enum):
    GENERAL = "general"
    ALL = "all"

class MediaManager:

    def __init__(self):
        self._engine = sa.create_engine('sqlite:////media/Projects/MediaStack/test.db', connect_args={'check_same_thread': False})
        Base.metadata.create_all(bind=self._engine)
        self._session_maker = sa.orm.sessionmaker(bind=self._engine)
        self._session = self._session_maker()
    
        self._media_initializer = MediaInitializer(self._session)
        self._media_initializer.initialize_media_from_disk();

        self._search_manager = SearchManager()

    def find_media(self, media_hash: str) -> Media:
        return self._session.query(Media).get(media_hash)

    def search(self, media_set: MediaSet, criteria: List[str] = []) -> List[Media]:
        start_time = time.time()
        if media_set == MediaSet.GENERAL:
            search_result = self._search_manager.search(self._get_media_set(media_set), criteria, self._get_album_set(media_set))
        elif media_set == MediaSet.ALL:
            search_result = self._search_manager.search(self._get_media_set(media_set), criteria)
        self._session.rollback()
        search_result.sort()
        print("Search took", time.time() - start_time, "to run")
        return search_result

    def _get_media_set(self, media_set: MediaSet) -> List[Media]:
        if (media_set == MediaSet.GENERAL):
            return list(self._session.query(Media).filter(Media.album == None, Media.path is not None))
        if (media_set == MediaSet.ALL):
            return list(self._session.query(Media).filter(Media.path is not None))

    def _get_album_set(self, media_set: MediaSet) -> List[Album]:
        if (media_set == MediaSet.GENERAL):
            return self._session.query(Album).all()
        if (media_set == MediaSet.ALL):
            return []
    

    