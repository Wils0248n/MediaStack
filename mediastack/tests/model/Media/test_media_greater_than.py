import unittest
from mediastack.model.Media import Media

class TestMediaGreaterThan(unittest.TestCase):
    def test_same_media(self):
        media = Media()
        media.hash = "hash"
        media.path = "1"
        self.assertFalse(media > media)

    def test_media_less_than_other(self):
        media = Media()
        media.hash = "hash"
        media.path = "1"

        other = Media()
        other.hash = "hash2"
        other.path = "2"
        self.assertFalse(media > other)

    def test_media_greater_than_other(self):
        media = Media()
        media.hash = "hash"
        media.path = "1"

        other = Media()
        other.hash = "hash2"
        other.path = "0"
        self.assertTrue(media > other)

    def test_other_is_none(self):
        media = Media()
        media.hash = "hash"
        media.path = "1"
        self.assertTrue(media > None)
    
    def test_other_has_no_path(self):
        media = Media()
        media.hash = "hash"
        media.path = "1"

        other = Media()
        other.hash = "hash2"
        self.assertTrue(media > None)