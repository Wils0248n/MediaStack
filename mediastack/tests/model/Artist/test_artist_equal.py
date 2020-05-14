import unittest
from mediastack.model.Artist import Artist

class TestArtistEqualTo(unittest.TestCase):
    def test_same_artist(self):
        artist = Artist("artist")
        self.assertTrue(artist == artist)

    def test_same_name(self):
        artist = Artist("artist")
        other = Artist("artist")
        self.assertTrue(artist == other)

    def test_other_is_none(self):
        artist = Artist("artist")
        self.assertFalse(artist == None)
