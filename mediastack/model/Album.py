from model import Media


class Album:
    def __init__(self, media: Media):
        self.name = media.album
        self.media_list = []
        self.add_media(media)

    def add_media(self, media: Media):
        self.media_list.append(media)

    def get_cover(self) -> Media:
        return None if len(self.media_list) == 0 else self.media_list[0]

