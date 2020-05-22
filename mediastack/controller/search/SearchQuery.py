from typing import List
from mediastack.model import *

class SearchQuery():
    def __init__(self):
        self.whitelist_tags: List[Tag] = []
        self.blacklist_tags: List[Tag] = []

        self.artist_restriction: Artist = None
        self.category_restriction: Category = None
        self.album_restriction: Album = None
        self.blacklist_artits: List[Artist] = []
        self.blacklist_categories: List[Category] = []
        self.blacklist_albums: List[Album] = []
    