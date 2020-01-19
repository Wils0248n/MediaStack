from Media import Media


class Album:
    def __init__(self, cover_media: Media):
        self.name = cover_media.album
        self.cover = cover_media
        self.media_list = []
        self.add_media(self.cover)

    def add_media(self, media: Media):
        self.media_list.append(media)

