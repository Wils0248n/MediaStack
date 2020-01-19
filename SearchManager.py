from Media import Media
from typing import List, Set


class SearchManager:
    def __init__(self):
        pass

    def search(self, media_list: List[Media], query_list: List[str]) -> List[Media]:
        special_queries = self.__get_special_queries(query_list)
        tag_queries = set(query_list).difference(special_queries)

        new_media_set = self.__get_media_from_special_queries(media_list, special_queries)
        new_media_set = self.__get_media_from_tag_queries(new_media_set, tag_queries)

        return list(new_media_set)

    def __get_special_queries(self, query_tags: List[str]) -> Set[str]:
        special_queries = set()
        for tag in query_tags:
            if ':' in tag:
                special_queries.add(tag)
        return special_queries

    def __get_media_from_special_queries(self, media_list: List[Media], special_queries: List[str]) -> Set[Media]:
        new_media_set = set(media_list)

        if len(special_queries) == 0:
            return new_media_set

        for query in special_queries:
            query_type = query.split(":")[0].lower()
            query_query = query.split(":")[1].lower()

            if query_type == "type":
                new_media_set = {media for media in new_media_set if media.type is not None and
                                 media.type.lower() == query_query.replace(' ', '_')}
            elif query_type == "category":
                new_media_set = {media for media in new_media_set if media.category is not None and
                                 media.category.replace('_', ' ').lower() == query_query}
            elif query_type == "artist":
                new_media_set = {media for media in new_media_set if media.artist is not None and
                                 media.artist.replace('_', ' ').lower() == query_query}
            elif query_type == "album":
                new_media_set = {media for media in new_media_set if media.album is not None and
                                 media.album.replace('_', ' ').lower() == query_query}
            elif query_type == "source":
                pass

        return new_media_set

    def __get_media_from_tag_queries(self, media_set: Set[Media], tag_queries: List[str]) -> Set[Media]:
        if len(tag_queries) == 0:
            return media_set

        whitelist_tags = []
        blacklist_tags = []
        for tag in tag_queries:
            if tag[0] == "-":
                blacklist_tags.append(tag[1:])
            else:
                whitelist_tags.append(tag)
        new_media_set = self.__get_media_that_contains_tags(media_set, whitelist_tags)
        new_media_set = self.__remove_media_that_does_not_contain_all_tags(new_media_set, whitelist_tags)
        new_media_set = self.__remove_media_that_contains_tags(media_set, new_media_set, blacklist_tags)
        return new_media_set

    def __get_media_that_contains_tags(self, media_list: Set[Media], tags: List[str]) -> Set[Media]:
        new_media_set = set()
        for media in media_list:
            for tag in tags:
                if tag in media.tags:
                    new_media_set.add(media)
        return new_media_set

    def __remove_media_that_does_not_contain_all_tags(self, media_set: Set[Media], tags: List[str]) -> Set[Media]:
        return {media for media in media_set if self.__does_media_contain_all_tags(media, tags)}

    def __remove_media_that_contains_tags(self, media_list: List[Media], media_set: Set[Media], tags: List[str]) \
            -> Set[Media]:
        return media_set.difference(self.__get_media_that_contains_tags(media_list, tags))

    def __does_media_contain_all_tags(self, media: Media, tags: List[str]) -> bool:
        for tag in tags:
            if tag not in media.tags:
                return False
        return True
