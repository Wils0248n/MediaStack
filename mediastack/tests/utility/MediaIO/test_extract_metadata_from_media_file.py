import unittest, os
from mediastack.utility.MediaIO import MediaIO

class TestExtractMetadataFromMediaFile(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self._previous_cwd = os.getcwd()
        os.chdir("mediastack/tests/")
        self._mediaio = MediaIO()

    @classmethod
    def tearDownClass(self):
        os.chdir(self._previous_cwd)

    def test_extract_metadata_from_non_existant_file(self):
        self.assertIsNone(self._mediaio.extract_metadata_from_media_file("non_existant_file.txt"))

    def test_extract_metadata_from_image(self):
        expected = {
            'album': None,
            'artist': 'input_artist',
            'category': 'input',
            'hash': 'd63f614e336fec57117d74b14aad1702',
            'score': 2,
            'source': "google",
            'tags': ['dog', 'white'],
            'type': 'image'
        }
        result = self._mediaio.extract_metadata_from_media_file("media/input/input_artist/image_3.jpg")
        self.assertEqual(expected, result)

    def test_extract_metadata_from_image_with_no_score_no_source_no_tags_in_album(self):
        expected = {
            'album': 'cat_album',
            'artist': 'input_artist',
            'category': 'input',
            'hash': '2550bc86af322d4e84e3c6a6480f8d4f',
            'score': 0,
            'source': None,
            'tags': [],
            'type': 'image'
        }
        result = self._mediaio.extract_metadata_from_media_file("media/input/input_artist/cat_album/image_1.jpg")
        self.assertEqual(expected, result)

    def test_extract_metadata_from_animated_image_in_album(self):
        expected = {
            'album': 'cat_album',
            'artist': 'input_artist',
            'category': 'input',
            'hash': 'f348d49188a34525ebdb3587a27eb9c5',
            'score': 0,
            'source': None,
            'tags': [],
            'type': 'animated_image'
        }
        result = self._mediaio.extract_metadata_from_media_file("media/input/input_artist/cat_album/image_2.gif")
        self.assertEqual(expected, result)
    
    def test_extract_metadata_from_video_in_album(self):
        expected = {
            'album': 'cat_album',
            'artist': 'input_artist',
            'category': 'input',
            'hash': '84648e4adbce47124bfea1348b9286ba',
            'score': 0,
            'source': None,
            'tags': [],
            'type': 'video'
        }
        result = self._mediaio.extract_metadata_from_media_file("media/input/input_artist/cat_album/video_1.mp4")
        self.assertEqual(expected, result)