from model.Media import Media

class Category:
    def __init__(self, name: str):
        self.name = name
        self.media_list = []

    def add_media(self, media: Media):
        if media not in self.media_list:
            self.media_list.append(media)
    
    def __repr__(self):
        return self.name