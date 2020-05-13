import unittest
from mediastack.utility.InputSanitizer import sanitize_input

class TestSanitizeInput(unittest.TestCase):

    def test_good_input(self):
        input = "hello"
        self.assertEqual(input, sanitize_input(input))

    def test_sanitized_input(self):
        self.assertEqual("hello_", sanitize_input("hello "))