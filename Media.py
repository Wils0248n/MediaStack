import errno
import os
import hashlib
import logging
import filetype
from typing import List
from enum import Enum
from iptcinfo3 import IPTCInfo

logging.getLogger('iptcinfo').setLevel(logging.ERROR)


class Media:

    def __init__(self, file_path: str, media_hash: str = None, media_type: str = None, category: str = None,
                 artist: str = None, album: str = None, source: str = None, tags: List[str] = None):
        self.path = file_path
        self.hash = media_hash
        self.type = media_type
        self.category = category
        self.artist = artist
        self.album = album
        self.tags = tags
        self.source = source
        self.__initialize_media_data()

    def __initialize_media_data(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.path)
        if self.hash is None:
            self.__update_hash()
        if self.type is None:
            media_type = self.determine_file_type()
            if media_type is None:
                raise ValueError("Unable to Determine Media Type for: " + self.path)
            else:
                self.type = media_type
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
            raise ValueError("Invalid media path: " + self.path)
        if self.source is None:
            self.__update_source()
        if self.tags is None:
            self.__update_tags()

    def __update_hash(self):
        hasher = hashlib.md5()
        with open(self.path, 'rb') as file:
            buffer = file.read()
            hasher.update(buffer)
        self.hash = hasher.hexdigest()

    def __update_tags(self):
        info = IPTCInfo(self.path)
        keywords = []
        for keyword in info['keywords']:
            keywords.append(keyword.decode("utf-8").lower())
        self.tags = keywords

    def __update_source(self):
        source = IPTCInfo(self.path)['caption/abstract']
        if source is not None:
            self.source = source.decode("utf-8")

    def determine_file_type(self):  # TODO: use type hint.
        file_type = filetype.guess(self.path)
        if file_type is not None:
            file_type = file_type.extension
            if file_type == "jpg" or file_type == "png":
                return Media.Type.IMAGE
            if file_type == "gif":
                return Media.Type.ANIMATED_IMAGE
            if file_type == "mp4" or file_type == "webm":
                return Media.Type.VIDEO
        return None

    def __str__(self):
        return self.hash + ", " + str(self.path) + ", " + str(self.category) + ", " \
               + str(self.artist) + ", " + str(self.album) + ", " + str(self.source) + ", " + str(self.tags)

    def __lt__(self, other):
        if self.category == other.category:
            return self.path < other.path
        else:
            return self.category < other.category

    def __gt__(self, other):
        if self.category == other.category:
            return self.path > other.path
        else:
            return self.category > other.category

    class Type(Enum):
        IMAGE = "image"
        ANIMATED_IMAGE = "animated_image"
        VIDEO = "video"
