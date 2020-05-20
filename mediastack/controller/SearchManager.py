import sqlalchemy as sa
from typing import List, Set, Dict
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag
from mediastack.controller.MediaSet import MediaSet

class SearchManager:

    def __init__(self, session: sa.orm.Session):
        self._session: sa.orm.Session = session
        self._media_list: List[Media] = []
        self._album_list: List[Album] = []
        self._criteria: List[str] = None

    def search(self, media_set: str, query_list: List[str]) -> List[Media]:
        media_set = MediaSet(media_set.lower())
        if media_set is None:
            None

        self._criteria = query_list

        if media_set == MediaSet.GENERAL:
            self._media_list = list(self._session.query(Media).filter(Media.album == None, Media.path != None))
            self._album_list = list(self._session.query(Album).filter(Album.cover != None))
            self._album_list = [album for album in self._album_list if album.cover != None and album.cover.path != None]
        elif media_set == MediaSet.ALL:
            self._media_list = list(self._session.query(Media).filter(Media.path != None))
            self._album_list = []

        if query_list is None or len(query_list) == 0:
            return self._media_list + [album.cover for album in self._album_list]

        special_queries = self._get_special_queries(query_list)
        tag_queries = set(query_list).difference(special_queries)

        if len(special_queries) == 0 and len(tag_queries) == 0 or query_list[0] == '':
            return self._media_list + [album.cover for album in self._album_list]

        self._filter_media(special_queries, tag_queries)
        self._filter_albums(special_queries, tag_queries)

        return self._media_list + [album.cover for album in self._album_list]

    def _get_special_queries(self, query_tags: List[str]) -> Set[str]:
        special_queries = set()
        for tag in query_tags:
            if ':' in tag:
                special_queries.add(tag)
        return special_queries

    def _filter_media(self, special_queries, tag_queries):
        self._filter_media_by_special_queries(special_queries)
        self._filter_media_by_tag_queries(tag_queries)

    def _filter_media_by_special_queries(self, special_queries: List[str]):
        if len(special_queries) == 0 or len(self._media_list) == 0:
            return

        for query in special_queries:
            query_type = query.split(":")[0].lower()
            query_query = query.split(":")[1].lower()

            if query_type == "type":
                self._media_list = [media for media in self._media_list  if media.type is not None and
                                 media.type.lower() == query_query]
            elif query_type == "category":
                self._media_list  = [media for media in self._media_list  if media.category_name is not None and
                                 str(media.category).lower() == query_query]
            elif query_type == "artist":
                self._media_list  = [media for media in self._media_list  if media.artist_name is not None and
                                 str(media.artist).lower() == query_query]
            elif query_type == "album":
                self._media_list  = [media for media in self._media_list if media.album_name is not None and
                                 str(media.album).lower() == query_query]
            elif query_type == "rating":
                try:
                    score = int(query_query)
                except:
                    self._media_list = []
                self._media_list = [media for media in self._media_list if media.score == score]

    def _filter_media_by_tag_queries(self, tag_queries: List[str]):
        if len(tag_queries) == 0 or len(self._media_list) == 0:
            return

        whitelist_tags = []
        blacklist_tags = []
        for tag_query in tag_queries:
            if tag_query[0] == "-":
                blacklist_tags.append(tag_query[1:])
            else:
                whitelist_tags.append(tag_query)

        for tag_name in whitelist_tags:
            current_tag = self._session.query(Tag).get(tag_name)
            if current_tag is None:
                self._media_list = []
            self._media_list = [media for media in self._media_list if current_tag in media.tags]

        for tag_name in blacklist_tags:
            current_tag = self._session.query(Tag).get(tag_name)
            if current_tag is None:
                self._media_list = []
            self._media_list = [media for media in self._media_list if current_tag not in media.tags]

    def _filter_albums(self, special_queries, tag_queries):
        self._filter_albums_by_special_queries(special_queries)
        self._filter_albums_by_tag_queries(tag_queries)

    def _filter_albums_by_special_queries(self, special_queries: List[str]):
        if len(special_queries) == 0 or len(self._album_list) == 0:
            return

        for query in special_queries:
            query_type = query.split(":")[0].lower()
            query_query = query.split(":")[1].lower()

            if query_type == "type":
                self._album_list = [album for album in self._album_list  if album.cover.type is not None and
                                 album.cover.type.lower() == query_query]
            elif query_type == "category":
                self._album_list  = [album for album in self._album_list  if album.cover.category_name is not None and
                                 str(album.cover.category_name).lower() == query_query]
            elif query_type == "artist":
                self._album_list  = [album for album in self._album_list  if album.cover.artist_name is not None and
                                 str(album.cover.artist_name).lower() == query_query]
            elif query_type == "album":
                self._album_list  = [album for album in self._album_list if album.name is not None and
                                 str(album.name).lower() == query_query]
            elif query_type == "rating":
                try:
                    score = int(query_query)
                except:
                    self._album_list = []
                self._album_list = [album for album in self._album_list if album.cover.score == score]
            
    def _filter_albums_by_tag_queries(self, tag_queries: List[str]):
        if len(tag_queries) == 0 or len(self._album_list) == 0:
            return

        whitelist_tags = []
        blacklist_tags = []
        for tag_query in tag_queries:
            if tag_query[0] == "-":
                blacklist_tags.append(tag_query[1:])
            else:
                whitelist_tags.append(tag_query)

        for tag_name in whitelist_tags:
            current_tag = self._session.query(Tag).get(tag_name)
            if current_tag is None:
                self._album_list = []
            self._album_list = [album for album in self._album_list if current_tag in album.tags]

        for tag_name in blacklist_tags:
            current_tag = self._session.query(Tag).get(tag_name)
            if current_tag is None:
                self._album_list = []
            self._album_list = [album for album in self._album_list if current_tag not in album.tags]
    