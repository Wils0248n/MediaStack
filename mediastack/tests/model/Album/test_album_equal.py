import unittest
from mediastack.model.Album import Album

class TestAlbumEqualTo(unittest.TestCase):
    def test_same_album(self):
        album = Album("album")
        self.assertTrue(album == album)

    def test_same_name(self):
        album = Album("album")
        other = Album("album")
        self.assertTrue(album == other)

    def test_other_is_none(self):
        album = Album("album")
        self.assertFalse(album == None)
    
    