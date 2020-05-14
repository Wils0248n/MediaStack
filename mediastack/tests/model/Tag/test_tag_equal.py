import unittest
from mediastack.model.Tag import Tag

class TestTagEqualTo(unittest.TestCase):
    def test_same_tag(self):
        tag = Tag("tag")
        self.assertTrue(tag == tag)

    def test_same_name(self):
        tag = Tag("tag")
        other = Tag("tag")
        self.assertTrue(tag == other)

    def test_other_is_none(self):
        tag = Tag("tag")
        self.assertFalse(tag == None)
