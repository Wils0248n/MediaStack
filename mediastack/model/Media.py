import os
from typing import List
from enum import Enum
from utility.MediaUtility import hash_file, extract_source, determine_media_type


class Media:

    def __init__(self, file_path: str, media_hash: str = None, media_type: Enum = None, category = None,
                 artist = None, album = None, source: str = None, tags = []):
        self.path = file_path
        self.hash = media_hash or hash_file(self.path)
        self.type = media_type or determine_media_type(self.path)
        self.category = category
        self.artist = artist
        self.album = album
        self.tags = tags
        self.source = source or extract_source(self.path)

    def __str__(self):
        return self.hash + ", " + str(self.path) + ", " + str(self.category) + ", " \
               + str(self.artist) + ", " + str(self.album) + ", " + str(self.source) + ", " + str(self.tags)

    def __lt__(self, other):
        if self.category == other.category:
            return self.path < other.path
        else:
            return self.category.name < other.category.name

    def __gt__(self, other):
        if self.category == other.category:
            return self.path > other.path
        else:
            return self.category.name > other.category.name


