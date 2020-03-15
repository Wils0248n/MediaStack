import sqlalchemy as sa
from typing import List
from mediastack.model.Base import Base
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag
from mediastack.utility.MediaIO import MediaIO
from mediastack.utility.MediaInitializer import MediaInitializer
from mediastack.utility.InputSanitizer import sanitize_input
from mediastack.controller.SearchManager import SearchManager
from mediastack.controller.MediaSet import MediaSet

class MediaManager:

    def __init__(self):
        self._engine = sa.create_engine('sqlite:///MediaStack.db', connect_args={'check_same_thread': False})
        Base.metadata.create_all(bind=self._engine)
        self._session_maker = sa.orm.sessionmaker(bind=self._engine)
        self._session = self._session_maker()
    
        self._mediaio = MediaIO()

        self._media_initializer = MediaInitializer(self._session, self._mediaio)
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
        if media is None or tag_name is None or len(tag_name) == 0:
            return
        tag_name = sanitize_input(tag_name)
        tag = self.find_tag(tag_name)
        if media.album is not None and media.album.cover == media:
            for media in media.album.media:
                media.tags.append(tag)
                self._mediaio.writeIPTCInfoToImage(media, "thumbs/")
        else:
            media.tags.append(tag)
            self._mediaio.writeIPTCInfoToImage(media, "thumbs/")
        self._session.commit()

    def remove_tag(self, media: Media, tag_name: str):
        if media is None or tag_name is None or len(tag_name) == 0:
            return
        tag_name = sanitize_input(tag_name)
        tag = self.find_tag(tag_name)
        if tag in media.tags:
            media.tags.remove(tag)
        self._mediaio.writeIPTCInfoToImage(media, "thumbs/")
        self._session.commit()

    def change_source(self, media: Media, new_source: str):
        if media is None or new_source is None or len(new_source) == 0:
            return
        try:
            media.source = new_source
            self._mediaio.writeIPTCInfoToImage(media, "thumbs/")
            self._session.commit()
        except:
            print("Error occured when changing source of " + media.path)

    def change_score(self, media: Media, new_score: str):
        if media is None or new_score is None or len(new_score) == 0:
            return
        try:
            if media.album_name is not None and media.album.cover == media:
                for album_media in media.album.media:
                    album_media.score = int(new_score)
            else:
                media.score = int(new_score)
            self._mediaio.writeIPTCInfoToImage(media, "thumbs/")
            self._session.commit()
        except:
            print("Error occured when changing score of " + media.path)

    def search(self, media_set: str, criteria: List[str] = []) -> List[Media]:
        search_result = self._search_manager.search(self._session, self.find_media_set(media_set), criteria)
        search_result.sort()
        return search_result

    def find_media_set(self, set_string: str) -> MediaSet:
        if set_string is None:
            return MediaSet.GENERAL
        media_set = MediaSet(set_string.lower())
        if media_set is None:
            return MediaSet.GENERAL
        return media_set