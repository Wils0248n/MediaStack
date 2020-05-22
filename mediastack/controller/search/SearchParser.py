import sqlalchemy as sa
from typing import List, Tuple
from mediastack.model.Tag import Tag
from mediastack.model.Album import Album
from mediastack.model.Artist import Artist
from mediastack.model.Category import Category
from mediastack.controller.search.SearchQuery import SearchQuery

SEARCH_QUERY_DELIMITER = ' '
BLACKLIST_QUERY_IDENTIFIER = '-'
SPECIAL_QUERY_IDENTIFIER = ':'

SPECIAL_ARTIST_QUERY_IDENTIFIER = "artist"
SPECIAL_ALBUM_QUERY_IDENTIFIER = "album"
SPECIAL_CATEGORY_QUERY_IDENTIFIER = "category"

class SearchError(Exception):
    pass

class SearchParser():
    
    def __init__(self, session: sa.orm.session):
        self._session = session

    def parse_search_query(self, query_string: str) -> SearchQuery:
        if query_string is None:
            return SearchQuery()
        query_string = self._sanitize_input(query_string)
        search_query = self._get_search_query(query_string)

        return search_query

    def _sanitize_input(self, input: str) -> str:
        return input.lower()

    def _get_search_query(self, query_string: str) -> SearchQuery:
        search_query = SearchQuery()
        for query in query_string.split(SEARCH_QUERY_DELIMITER):
            if SPECIAL_QUERY_IDENTIFIER in query:
                query_id, query_value = self._extract_special_query_values(query)
                if BLACKLIST_QUERY_IDENTIFIER in query:
                    if query_id == SPECIAL_ARTIST_QUERY_IDENTIFIER:
                        artist = self._session.query(Artist).get(query_value)
                        if artist is None:
                            raise SearchError("Blacklisted artist not found: " + query_value)
                        search_query.blacklist_artits.append(artist)
                    elif query_id == SPECIAL_ALBUM_QUERY_IDENTIFIER:
                        album = self._session.query(Album).get(query_value)
                        if album is None:
                            raise SearchError("Blacklisted album not found: " + query_value)
                        search_query.blacklist_albums.append(query_value)
                    elif query_id == SPECIAL_CATEGORY_QUERY_IDENTIFIER:
                        category = self._session.query(Category).get(query_value)
                        if category is None:
                            raise SearchError("Blacklisted category not found: " + query_value)
                        search_query.blacklist_categories.append(query_value)
                else:
                    if query_id == SPECIAL_ARTIST_QUERY_IDENTIFIER:
                        if search_query.artist_restriction is not None:
                            raise SearchError("Duplicate artist restriction: " + query_value)
                        artist = self._session.query(Artist).get(query_value)
                        if artist is None:
                            raise SearchError("Artist not found: " + query_value)
                        search_query.artist_restriction = artist
                    elif query_id == SPECIAL_ALBUM_QUERY_IDENTIFIER:
                        if search_query.album_restriction is not None:
                            raise SearchError("Duplicate album restriction: " + query_value)
                        album = self._session.query(Album).get(query_value)
                        if album is None:
                            raise SearchError("Album not found: " + query_value)
                        search_query.album_restriction = album
                    elif query_id == SPECIAL_CATEGORY_QUERY_IDENTIFIER:
                        if search_query.category_restriction is not None:
                            raise SearchError("Duplicate category restriction: " + query_value)
                        category = self._session.query(Category).get(query_value)
                        if category is None:
                            raise SearchError("Category not found: " + query_value)
                        search_query.category_restriction = category
            elif BLACKLIST_QUERY_IDENTIFIER in query:
                tag = self._session.query(Tag).get(query[1:])
                if tag is None:
                    raise SearchError("Tag not found: " + query)
                search_query.blacklist_tags.append(tag)
            else:
                tag = self._session.query(Tag).get(query)
                if tag is None:
                    raise SearchError("Tag not found: "  + query)
                search_query.whitelist_tags.append(tag)
        return search_query
    
    def _extract_special_query_values(self, special_query: str) -> Tuple[str, str]:
        if special_query[0] == BLACKLIST_QUERY_IDENTIFIER:
            special_query = special_query[1:]

        query_split = special_query.split(SPECIAL_QUERY_IDENTIFIER)
        return query_split[0], query_split[1]
    