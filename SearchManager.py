from Media import Media
from typing import List, Set


class SearchManager:
    def __init__(self):
        pass

    def search(self, media_list: List[Media], tags: List[str]) -> List[Media]:
        whitelist_tags = []
        blacklist_tags = []

        for tag in tags:
            if tag[0] == "-":
                blacklist_tags.append(tag[1:])
            else:
                whitelist_tags.append(tag)

        new_media_set = self.__get_media_that_contains_tags(media_list, whitelist_tags)
        new_media_set = self.__remove_media_that_does_not_contain_all_tags(new_media_set, whitelist_tags)
        new_media_set = self.__remove_media_that_contains_tags(media_list, new_media_set, blacklist_tags)

        return list(new_media_set)

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