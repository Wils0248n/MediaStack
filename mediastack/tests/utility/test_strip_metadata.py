import unittest, os
from shutil import copyfile
from mediastack.utility.MediaIO import MediaIO

class TestStripMetadata(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._previous_cwd = os.getcwd()
        os.chdir("mediastack/tests/")
        self._mediaio = MediaIO()
        self._image_with_metadata = "media/output/image_3.jpg"
        copyfile("media/input/input_artist/image_3.jpg", self._image_with_metadata)

    @classmethod
    def tearDownClass(self):
        os.remove(self._image_with_metadata)
        os.chdir(self._previous_cwd)

    def test_strip_metadata_from_file_with_metadata(self):
        pre_strip = {
            'album': None,
            'artist': None,
            'category': 'output',
            'hash': 'd63f614e336fec57117d74b14aad1702',
            'score': 2,
            'source': "google",
            'tags': ['dog', 'white'],
            'type': 'image'
        }
        self.assertEqual(pre_strip, self._mediaio.extract_metadata_from_media_file(self._image_with_metadata))
        self._mediaio.strip_metadata(self._image_with_metadata)
        post_strip = self._mediaio.extract_metadata_from_media_file(self._image_with_metadata)
        self.assertIsNone(post_strip["source"])
        self.assertEqual(0, post_strip["score"])
        self.assertEqual([], post_strip["tags"])

    def test_strip_metadata_from_non_existant_file(self):
        with self.assertRaises(FileNotFoundError):
            self._mediaio.strip_metadata("non_existant_file.txt")
    