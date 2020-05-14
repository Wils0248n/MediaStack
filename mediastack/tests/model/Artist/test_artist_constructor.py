import unittest
from mediastack.model.Artist import Artist

class TestArtistConstructor(unittest.TestCase):
    def test_with_good_name(self):
        artist = Artist("artist_name")
        self.assertEqual("artist_name", artist.name)

    def test_name_is_none(self):
        with self.assertRaises(ValueError):
            Artist(None)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Artist("")