from model.Media import Media

class Tag:
    def __init__(self, name):
        self.name = name
        self.media_list = []

    def add_media(self, media: Media):
        if media not in self.media_list:
            self.media_list.append(media)

    def number_of_media(self):
        return len(self.media_list)

    def __eq__(self, other):
        return self.name == str(other)

    def __repr__(self):
        return self.name