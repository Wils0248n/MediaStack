import unittest
from mediastack.model.Category import Category

class TestCategoryConstructor(unittest.TestCase):
    def test_with_good_name(self):
        category = Category("category_name")
        self.assertEqual("category_name", category.name)

    def test_name_is_none(self):
        with self.assertRaises(ValueError):
            Category(None)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Category("")