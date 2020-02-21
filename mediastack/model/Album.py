class Album:
    def __init__(self, name: str):
        self.name = name
        self.media_list = []

    def add_media(self, media):
        self.media_list.append(media)

    def get_index(self, media):
        return self.media_list.index(media)

    def get_cover(self):
        return None if len(self.media_list) == 0 else self.media_list[0]

    def __repr__(self):
        return self.name