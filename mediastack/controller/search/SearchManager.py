import sqlalchemy as sa
from typing import List, Set, Dict
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag
from mediastack.controller.search.MediaSet import MediaSet
from mediastack.controller.search.SearchParser import SearchParser, SearchError
from mediastack.controller.search.SearchQuery import SearchQuery

class SearchManager:

    def __init__(self, session: sa.orm.Session):
        self._session: sa.orm.Session = session
        self._search_parser = SearchParser(self._session)
        self._media_list: List[Media] = []
        self._album_list: List[Album] = []
        self._criteria: List[str] = None

    def search(self, media_set: str, search_query_string: str) -> List[Media]:
        try:
            media_set = MediaSet(media_set.lower())
        except ValueError:
            raise SearchError("Invalid media set.")
            
        try:
            search_query = self._search_parser.parse_search_query(search_query_string)
        except SearchError:
            return []

        self._media_list = list(self._find_base_media(media_set, search_query))
        self._album_list = list(self._find_base_albums(media_set, search_query))

        for tag in search_query.whitelist_tags:
            self._media_list = [media for media in self._media_list if tag in media.tags]
            self._album_list = [album for album in self._album_list if tag in album.tags]

        for tag in search_query.blacklist_tags:
            self._media_list = [media for media in self._media_list if tag not in media.tags]
            self._album_list = [album for album in self._album_list if tag not in album.tags]

        return self._media_list + [album.cover for album in self._album_list]

    def _find_base_media(self, media_set: MediaSet, search_query: SearchQuery) -> List[Media]:
        if media_set is MediaSet.ALL:
            if search_query.album_restriction is not None:
                return self._session.query(Media).filter(Media.path != None, Media.album == search_query.album_restriction)
            if search_query.artist_restriction is not None:
                return self._session.query(Media).filter(Media.path != None, Media.artist_name == search_query.artist_restriction.name)
            if search_query.category_restriction is not None:
                return self._session.query(Media).filter(Media.path != None, Media.category_name == search_query.category_restriction.name)
            if len(search_query.whitelist_tags) > 0:
                tag_media = self._session.query(Tag).filter(Tag.name == search_query.whitelist_tags[0].name).first().media
                return [media for media in tag_media if media.path is not None]
            return self._session.query(Media).filter(Media.path != None)
        elif media_set is MediaSet.MEDIA or media_set is MediaSet.GENERAL:
            if search_query.album_restriction is not None:
                return []
            if search_query.artist_restriction is not None:
                return self._session.query(Media).filter(Media.path != None, Media.album == None, Media.artist_name == search_query.artist_restriction.name)
            if search_query.category_restriction is not None:
                return self._session.query(Media).filter(Media.path != None, Media.album == None, Media.category_name == search_query.category_restriction.name)
            if len(search_query.whitelist_tags) > 0:
                tag_media = self._session.query(Tag).filter(Tag.name == search_query.whitelist_tags[0].name).first().media
                return [media for media in tag_media if media.path is not None and media.album is None]
            return self._session.query(Media).filter(Media.path != None, Media.album == None)
        elif media_set is MediaSet.ALBUMS:
            return []
        return None

    def _find_base_albums(self, media_set: MediaSet, search_query: SearchQuery) -> List[Album]:
        if media_set is MediaSet.ALL or media_set is MediaSet.MEDIA:
            return []
        if media_set is MediaSet.ALBUMS or MediaSet.GENERAL:
            if search_query.album_restriction is not None:
                return [search_query.album_restriction]
            return self._session.query(Album).all()
        return None
