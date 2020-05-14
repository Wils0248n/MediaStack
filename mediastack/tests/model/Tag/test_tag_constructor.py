import unittest
from mediastack.model.Tag import Tag

class TestTagConstructor(unittest.TestCase):
    def test_with_good_name(self):
        tag = Tag("tag_name")
        self.assertEqual("tag_name", tag.name)

    def test_name_is_none(self):
        with self.assertRaises(ValueError):
            tag = Tag(None)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            tag = Tag("")