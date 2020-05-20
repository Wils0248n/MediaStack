import unittest, os
from mediastack.utility.MediaIO import MediaIO

class TestMediaIOHashFile(unittest.TestCase):

    def test_hash_file(self):
        self.assertEqual("2550bc86af322d4e84e3c6a6480f8d4f", MediaIO.hash_file("mediastack/tests/media/input/input_artist/cat_album/image_1.jpg"))

    def test_hash_non_existant_file(self):
        with self.assertRaises(FileNotFoundError):
            MediaIO.hash_file("non_existant_file")