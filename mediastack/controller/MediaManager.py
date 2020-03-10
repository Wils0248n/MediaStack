import sqlalchemy as sa
from enum import Enum
from typing import List
from mediastack.model.Base import Base
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.controller.SearchManager import SearchManager
from mediastack.controller.MediaInitializer import MediaInitializer

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
        search_result = self._search_manager.search(self._get_media_set(media_set), criteria)
        search_result.sort()
        return search_result

    def _get_media_set(self, media_set: MediaSet) -> List[Media]:
        if (media_set == MediaSet.GENERAL):
            return self._get_general_media()
        if (media_set == MediaSet.ALL):
            return self._get_all_media()

    def _get_general_media(self) -> List[Media]:
        general_media = list(self._session.query(Media).filter(Media.album == None))
        for album in self._session.query(Album).all():
            general_media.append(album.cover)
        return general_media

    def _get_all_media(self) -> List[Media]:
        return self._session.query(Media).all()