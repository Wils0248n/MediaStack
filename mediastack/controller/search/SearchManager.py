import sqlalchemy as sa
from typing import List, Set, Dict
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag
from mediastack.controller.search.MediaSet import MediaSet
from mediastack.controller.search.SearchParser import SearchParser, SearchError
from mediastack.controller.search.SearchQuery import SearchQuery

class SearchManager:

    # TODO: This entire class is very inefficent, optimize.

    def __init__(self, session: sa.orm.Session):
        self._session: sa.orm.Session = session
        self._search_parser = SearchParser(self._session)
        self._media_list: List[Media] = []
        self._album_list: List[Album] = []
        self._criteria: List[str] = None

    def search(self, raw_search_query: Dict) -> List[Media]:
        try:
            search_query = self._search_parser.parse_search_query(raw_search_query)
        except SearchError:
            return [[], []]

        self._media_list = list(self._find_base_media(search_query))
        self._album_list = list(self._find_base_albums(search_query))

        for tag in search_query.whitelist_tags:
            self._media_list = [media for media in self._media_list if tag in media.tags]
            self._album_list = [album for album in self._album_list if tag in album.tags]

        for tag in search_query.blacklist_tags:
            self._media_list = [media for media in self._media_list if tag not in media.tags]
            self._album_list = [album for album in self._album_list if tag not in album.tags]

        for album in search_query.blacklist_albums:
            self._media_list = [media for media in self._media_list if media.album is not album]
            self._album_list = [album for album in self._album_list if album is not album]

        for artist in search_query.blacklist_artists:
            self._media_list = [media for media in self._media_list if media.artist != artist]
            self._album_list = [album for album in self._album_list if album.cover.artist != artist]

        for category in search_query.blacklist_categories:
            self._media_list = [media for media in self._media_list if media.category.name != category.name]
            self._album_list = [album for album in self._album_list if album.cover.category.name != category.name]

        if search_query.score_restriction is not None:
            self._media_list = [media for media in self._media_list if media.score is not None and media.score is not search_query.score_restriction]
            self._album_list = [album for album in self._album_list if album.score is not None and album.score is not search_query.score_restriction]

        if search_query.gt_score_restriction is not None:
            self._media_list = [media for media in self._media_list if media.score is not None and media.score > search_query.gt_score_restriction]
            self._album_list = [album for album in self._album_list if album.score is not None and album.score > search_query.gt_score_restriction]

        if search_query.lt_score_restriction is not None:
            self._media_list = [media for media in self._media_list if media.score is not None and media.score < search_query.lt_score_restriction]
            self._album_list = [album for album in self._album_list if album.score is not None and album.score < search_query.lt_score_restriction]

        if search_query.type_restriction is not None:
            self._media_list = [media for media in self._media_list if media.type is not None and media.type == search_query.type_restriction]
            self._album_list = [album for album in self._album_list if search_query.type_restriction in album.types]

        return (self._media_list, self._album_list)

    def _find_base_media(self, search_query: SearchQuery) -> List[Media]:
        if search_query.album_restriction is not None:
            return []
        if search_query.artist_restriction is not None:
            return self._session.query(Media).filter(Media.path != None, Media.album_name == None, Media.artist_name == search_query.artist_restriction.name)
        if search_query.category_restriction is not None:
            return self._session.query(Media).filter(Media.path != None, Media.album_name == None, Media.category_name == search_query.category_restriction.name)
        if len(search_query.whitelist_tags) > 0:
            tag_media = search_query.whitelist_tags[0].media
            return [media for media in tag_media if media.path is not None and media.album_name is None]
        return self._session.query(Media).filter(Media.path != None, Media.album_name == None)

    def _find_base_albums(self, search_query: SearchQuery) -> List[Album]:
        if search_query.album_restriction is not None:
            return [search_query.album_restriction]
        if search_query.artist_restriction is not None:
            return [album for album in self._session.query(Album).all() if album.cover.artist == search_query.artist_restriction]
        if search_query.category_restriction is not None:
            return [album for album in self._session.query(Album).all() if album.cover.category == search_query.category_restriction]
        if len(search_query.whitelist_tags) > 0:
            tag_albums = search_query.whitelist_tags[0].albums
            return [album for album in tag_albums if len(album.media) > 0]
        return self._session.query(Album).all()
