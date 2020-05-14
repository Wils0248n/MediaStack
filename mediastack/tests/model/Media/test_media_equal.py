import unittest
from mediastack.model.Media import Media

class TestMediaEqualTo(unittest.TestCase):
    def test_same_media(self):
        media = Media()
        media.hash = "hash"
        self.assertTrue(media == media)

    def test_same_hash(self):
        media = Media()
        media.hash = "hash"

        other = Media()
        other.hash = "hash"
        self.assertTrue(media == other)

    def test_other_is_none(self):
        media = Media()
        media.hash = "hash"
        media.path = "1"
        self.assertFalse(media == None)
    
    def test_other_has_no_hash(self):
        media = Media()
        media.hash = "hash"
        media.path = "1"

        other = Media()
        self.assertFalse(media == None)