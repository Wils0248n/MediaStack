class SearchManager:
    def __init__(self):
        pass

    def search(self, media_list, tags):
        whitelist_tags = []
        blacklist_tags = []

        for tag in tags:
            if tag[0] == "-":
                blacklist_tags.append(tag[1:])
            else:
                whitelist_tags.append(tag)

        new_media_set = self.get_media_that_contains_tags(media_list, whitelist_tags)
        new_media_set = self.remove_media_that_does_not_contain_all_tags(new_media_set, whitelist_tags)
        new_media_set = self.remove_media_that_contains_tags(media_list, new_media_set, blacklist_tags)

        return list(new_media_set)

    def get_media_that_contains_tags(self, media_list, tags):
        new_media_set = set()
        for media in media_list:
            for tag in tags:
                if tag in media.tags:
                    new_media_set.add(media)
        return new_media_set

    def remove_media_that_does_not_contain_all_tags(self, media_set, tags):
        return {media for media in media_set if self.does_media_contain_all_tags(media, tags)}

    def does_media_contain_all_tags(self, media, tags):
        for tag in tags:
            if tag not in media.tags:
                return False
        return True

    def remove_media_that_contains_tags(self, media_list, media_set, tags):
        return media_set.difference(self.get_media_that_contains_tags(media_list, tags))

