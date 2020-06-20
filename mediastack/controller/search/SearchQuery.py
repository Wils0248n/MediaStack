from typing import List
from mediastack.model import *

class SearchQuery():
    def __init__(self):
        self.whitelist_tags: List[Tag] = []
        self.blacklist_tags: List[Tag] = []

        self.score_restriction: int = None
        self.gt_score_restriction: int = None
        self.lt_score_restriction: int = None

        self.type_restriction: str = None

        self.artist_restriction: Artist = None
        self.category_restriction: Category = None
        self.album_restriction: Album = None

        self.blacklist_artists: List[Artist] = []
        self.blacklist_categories: List[Category] = []
        self.blacklist_albums: List[Album] = []
    