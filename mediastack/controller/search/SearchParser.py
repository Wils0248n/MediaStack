import sqlalchemy as sa
from typing import List, Tuple, Dict
from mediastack.model.Tag import Tag
from mediastack.model.Album import Album
from mediastack.model.Artist import Artist
from mediastack.model.Category import Category
from mediastack.controller.search.SearchQuery import SearchQuery

class SearchError(Exception):
    pass

class SearchParser():
    
    def __init__(self, session: sa.orm.session):
        self._session = session

    def parse_search_query(self, raw_search_query: Dict) -> SearchQuery:
        if raw_search_query is None:
            return SearchQuery()
        
        search_query = SearchQuery()

        self._extract_whitelist_tags(search_query, raw_search_query)
        self._extract_blacklist_tags(search_query, raw_search_query)

        self._extract_album(search_query, raw_search_query)
        self._extract_artist(search_query, raw_search_query)
        self._extract_category(search_query, raw_search_query)

        self._extract_score_restriction(search_query, raw_search_query)
        self._extract_gt_score_restriction(search_query, raw_search_query)
        self._extract_lt_score_restriction(search_query, raw_search_query)

        self._extract_type_restriction(search_query, raw_search_query)

        self._extract_blacklist_albums(search_query, raw_search_query)
        self._extract_blacklist_artists(search_query, raw_search_query)
        self._extract_blacklist_categories(search_query, raw_search_query)

        return search_query

    def _get_search_query(self, raw_search_query: Dict) -> SearchQuery:
        search_query = SearchQuery()

        return search_query

    def _extract_whitelist_tags(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            for tag_name in raw_search_query['whitelist_tags']:
                tag = self._session.query(Tag).get(tag_name)
                if tag is None:
                    raise SearchError("Could not find whitelist tag: " + tag_name)
                search_query.whitelist_tags.append(tag)
        except KeyError:
            pass

    def _extract_blacklist_tags(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            for tag_name in raw_search_query['blacklist_tags']:
                tag = self._session.query(Tag).get(tag_name)
                if tag is None:
                    raise SearchError("Could not find blacklist tag: " + tag_name)
                search_query.blacklist_tags.append(tag)
        except KeyError:
            pass

    def _extract_blacklist_albums(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            for album_name in raw_search_query['blacklist_albums']:
                album = self._session.query(Album).get(album_name)
                if album is None:
                    raise SearchError("Could not find blacklist album: " + album_name)
                search_query.blacklist_albums.append(album)
        except KeyError:
            pass

    def _extract_blacklist_artists(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            for artist_name in raw_search_query['blacklist_artists']:
                artist = self._session.query(Artist).get(artist_name)
                if artist is None:
                    raise SearchError("Could not find blacklist artist: " + artist_name)
                search_query.blacklist_artists.append(artist)
        except KeyError:
            pass

    def _extract_blacklist_categories(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            for category_name in raw_search_query['blacklist_categories']:
                category = self._session.query(Category).get(category_name)
                if category is None:
                    raise SearchError("Could not find blacklist category: " + category_name)
                search_query.blacklist_categories.append(category)
        except KeyError:
            pass

    def _extract_album(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            search_query.album_restriction = self._session.query(Album).get(raw_search_query['album'])
        except KeyError:
            pass

    def _extract_artist(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            search_query.artist_restriction = self._session.query(Artist).get(raw_search_query['artist'])
        except KeyError:
            pass

    def _extract_category(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            search_query.category_restriction = self._session.query(Category).get(raw_search_query['category'])
        except KeyError:
            pass
    
    def _extract_score_restriction(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            search_query.score_restriction = raw_search_query['score']
        except KeyError:
            pass

    def _extract_gt_score_restriction(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            search_query.gt_score_restriction = raw_search_query['score_greater_than']
        except KeyError:
            pass

    def _extract_lt_score_restriction(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            search_query.lt_score_restriction = raw_search_query['score_less_than']
        except KeyError:
            pass

    def _extract_type_restriction(self, search_query: SearchQuery, raw_search_query: Dict) -> None:
        try:
            search_query.type_restriction = raw_search_query['type']
        except KeyError:
            pass
    