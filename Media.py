import errno
import os
import hashlib
import logging
from iptcinfo3 import IPTCInfo
from PIL import Image, UnidentifiedImageError

logging.getLogger('iptcinfo').setLevel(logging.ERROR)


class Media:

    def __init__(self, file_path, media_hash=None, category=None, artist=None, album=None, source=None, tags=None):
        self.path = file_path
        self.hash = media_hash
        self.category = category
        self.artist = artist
        self.album = album
        self.tags = tags
        self.source = source
        self.initialize_media_data()

    def initialize_media_data(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        if self.hash is None:
            self.update_hash()
        try:
            if self.category is None:
                self.category = self.path.split(os.path.sep)[1]
            if self.artist is None:
                self.artist = self.path.split(os.path.sep)[2]
            if self.album is None:
                album_path = os.path.sep.join(self.path.split(os.path.sep)[:-1])
                album_name = self.path.split(os.path.sep)[3]
                if album_path + os.path.sep + album_name == self.path:
                    self.album = None
                else:
                    self.album = album_name
        except IndexError:
            raise ValueError("Invalid file_path")
        if self.source is None:
            self.update_source()
        if self.tags is None:
            self.update_tags()

    def update_hash(self):
        hasher = hashlib.md5()
        with open(self.path, 'rb') as file:
            buffer = file.read()
            hasher.update(buffer)
        self.hash = hasher.hexdigest()

    def update_tags(self):
        info = IPTCInfo(self.path)
        keywords = []
        for keyword in info['keywords']:
            keywords.append(keyword.decode("utf-8").lower())
        self.tags = keywords

    def update_source(self):
        source = IPTCInfo(self.path)['caption/abstract']
        if source is not None:
            self.source = source.decode("utf-8")

    def create_thumbnail(self, thumbnail_directory, width=225, height=175):
        if thumbnail_directory[-1] is not os.path.sep:
            thumbnail_directory += os.path.sep
        if os.path.isfile(thumbnail_directory + self.hash):
            return True
        try:
            image = Image.open(self.path)
        except UnidentifiedImageError:
            return False
        image.thumbnail((width, height))
        output_path = thumbnail_directory + self.hash
        image.save(output_path, format=image.format)
        return True

    def __str__(self):
        return self.hash + ", " + str(self.path) + ", " + str(self.category) + ", " \
               + str(self.artist) + ", " + str(self.album) + ", " + str(self.source) + ", " + str(self.tags)
