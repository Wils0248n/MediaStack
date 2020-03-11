import sqlalchemy as sa
from typing import List
from mediastack.model.Base import Base
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag
from mediastack.controller.SearchManager import SearchManager
from mediastack.controller.MediaInitializer import MediaInitializer
from mediastack.controller.MediaSet import MediaSet

import time

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
        if media_hash is None:
            return None;
        return self._session.query(Media).get(media_hash)

    def find_tag(self, tag_name: str) -> Tag:
        if tag_name is None:
            return None;
        tag = self._session.query(Tag).get(tag_name)
        if tag is None:
            tag = Tag(tag_name)
            self._session.add(tag)
        return tag

    def add_tag(self, media: Media, tag_name: str):
        tag = self.find_tag(tag_name)
        media.tags.append(tag)
        self._session.commit()

    def remove_tag(self, media: Media, tag_name: str):
        tag = self.find_tag(tag_name)
        if tag in media.tags:
            media.tags.remove(tag)
        self._session.commit()

    def change_source(self, media: Media, new_source: str):
        try:
            media.source = new_source
            self._session.commit()
        except:
            pass

    def change_score(self, media: Media, new_score: str):
        try:
            media.score = int(new_score)
            self._session.commit()
        except:
            pass

    def search(self, media_set: MediaSet, criteria: List[str] = []) -> List[Media]:
        start_time = time.time()
        search_result = self._search_manager.search(self._session, media_set, criteria)
        #self._session.rollback()
        search_result.sort()
        print("Search took", time.time() - start_time, "to run")
        return search_result

    

    