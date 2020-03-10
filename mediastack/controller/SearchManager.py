from typing import List, Set, Dict
from mediastack.model.Media import Media
from mediastack.model.Album import Album

class SearchManager:

    def search(self, media_list: List[Media], query_list: List[str], album_list: List[Album] = []) -> List[Media]:

        if query_list is None:
            return media_list + [album.cover for album in album_list]

        special_queries = self._get_special_queries(query_list)
        tag_queries = set(query_list).difference(special_queries)

        if len(special_queries) == 0 and len(tag_queries) == 0 or query_list[0] == '':
            return media_list + [album.cover for album in album_list]

        # The goal of passing an album list is to evaluate each album 
        # cover as if it has album.media_tags as its tags.
        # TODO: This is scuffed
        cover_list = []
        for album in album_list:
            cover = album.cover
            cover.tags += album.media_tags
            cover_list.append(cover)

        media_list = media_list + cover_list

        new_media_set = self._get_media_from_special_queries(media_list, special_queries)
        new_media_set = self._get_media_from_tag_queries(new_media_set, tag_queries)

        return list(new_media_set)

    def _get_special_queries(self, query_tags: List[str]) -> Set[str]:
        special_queries = set()
        for tag in query_tags:
            if ':' in tag:
                special_queries.add(tag)
        return special_queries

    def _get_media_from_special_queries(self, media_list: List[Media], special_queries: List[str]) -> Set[Media]:
        new_media_set = set(media_list)

        if len(special_queries) == 0:
            return new_media_set

        for query in special_queries:
            query_type = query.split(":")[0].lower()
            query_query = query.split(":")[1].lower()

            if query_type == "type":
                new_media_set = {media for media in new_media_set if media.type is not None and
                                 media.type.lower() == query_query}
            elif query_type == "category":
                new_media_set = {media for media in new_media_set if media.category_name is not None and
                                 str(media.category).lower() == query_query}
            elif query_type == "artist":
                new_media_set = {media for media in new_media_set if media.artist_name is not None and
                                 str(media.artist).lower() == query_query}
            elif query_type == "album":
                new_media_set = {media for media in new_media_set if media.album_name is not None and
                                 str(media.album).lower() == query_query}
            elif query_type == "source":
                pass

        return new_media_set

    def _get_media_from_tag_queries(self, media_set: Set[Media], tag_queries: List[str]) -> Set[Media]:
        if len(tag_queries) == 0:
            return media_set

        whitelist_tags = []
        blacklist_tags = []
        for tag_query in tag_queries:
            if tag_query[0] == "-":
                blacklist_tags.append(tag_query[1:])
            else:
                whitelist_tags.append(tag_query)
        new_media_set = self._get_media_that_contains_tags(media_set, whitelist_tags)
        new_media_set = self._remove_media_that_does_not_contain_all_tags(new_media_set, whitelist_tags)
        new_media_set = self._remove_media_that_contains_tags(media_set, new_media_set, blacklist_tags)
        return new_media_set

    def _get_media_that_contains_tags(self, media_list: Set[Media], tags: List[str]) -> Set[Media]:
        new_media_set = set()
        for media in media_list:
            for tag in tags:
                if tag in media.tags:
                    new_media_set.add(media)
        return new_media_set

    def _remove_media_that_does_not_contain_all_tags(self, media_set: Set[Media], tags: List[str]) -> Set[Media]:
        return {media for media in media_set if self._does_media_contain_all_tags(media, tags)}

    def _remove_media_that_contains_tags(self, media_list: List[Media], media_set: Set[Media], tags: List[str]) -> Set[Media]:
        return media_set.difference(self._get_media_that_contains_tags(media_list, tags))

    def _does_media_contain_all_tags(self, media: Media, tags: List[str]) -> bool:
        for tag in tags:
            if tag not in media.tags:
                return False
        return True
