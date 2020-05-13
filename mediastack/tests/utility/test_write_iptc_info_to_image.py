import unittest, os
from shutil import copyfile
from mediastack.utility.MediaIO import MediaIO
from mediastack.model.Media import Media
from mediastack.model.Tag import Tag

class TestWriteIPTCInfoToImage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._previous_cwd = os.getcwd()
        os.chdir("mediastack/tests/")

        self._mediaio = MediaIO()

        self._image_without_metadata = "media/output/image_1.jpg"
        copyfile("media/input/input_artist/cat_album/image_1.jpg", self._image_without_metadata)

    @classmethod
    def tearDownClass(self):
        os.remove(self._image_without_metadata)
        os.chdir(self._previous_cwd)

    def test_write_metadata_to_media_without_path(self):
        self._mediaio.write_iptc_info_to_media(Media())

    def test_write_metadata_to_media_without_hash(self):
        some_media = Media()
        some_media.path = self._image_without_metadata
        self._mediaio.write_iptc_info_to_media(some_media)

    def test_write_metadata_to_media(self):
        pre_write = {
            'album': None,
            'artist': None,
            'category': 'output',
            'hash': '2550bc86af322d4e84e3c6a6480f8d4f',
            'score': 0,
            'source': None,
            'tags': [],
            'type': 'image'
        }
        self.assertEqual(pre_write, self._mediaio.extract_metadata_from_media_file(self._image_without_metadata))
        media = Media()
        media.path = self._image_without_metadata
        media.hash = pre_write['hash']
        media.score = 3
        media.source = "google"
        media.tags.append(Tag("cat"))
        media.tags.append(Tag("brown"))
        self._mediaio.write_iptc_info_to_media(media)
        post_write = {
            'album': None,
            'artist': None,
            'category': 'output',
            'hash': '354f992beea79d5b22f74731cb56674a',
            'score': 3,
            'source': 'google',
            'tags': ['cat', 'brown'],
            'type': 'image'
        }
        self.assertEqual(post_write, self._mediaio.extract_metadata_from_media_file(self._image_without_metadata))
        self.assertFalse(os.path.isfile(self._image_without_metadata + "~"))