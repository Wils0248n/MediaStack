import unittest
from mediastack.model.Album import Album

class TestAlbumConstructor(unittest.TestCase):
    def test_with_good_name(self):
        album = Album("album_name")
        self.assertEqual("album_name", album.name)

    def test_name_is_none(self):
        with self.assertRaises(ValueError):
            album = Album(None)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            album = Album("")