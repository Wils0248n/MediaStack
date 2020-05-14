import unittest
from mediastack.model.Category import Category

class TestCategoryEqualTo(unittest.TestCase):
    def test_same_category(self):
        category = Category("category")
        self.assertTrue(category == category)

    def test_same_name(self):
        category = Category("category")
        other = Category("category")
        self.assertTrue(category == other)

    def test_other_is_none(self):
        category = Category("category")
        self.assertFalse(category == None)
