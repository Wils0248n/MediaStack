import unittest, os
import sqlalchemy as sa
from mediastack.model.Media import Media
from mediastack.utility.MediaIO import MediaIO
from mediastack.utility.Thumbnailer import Thumbnailer

class TestCreateThumbnail(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._thumbnailer = Thumbnailer("mediastack/tests/media/output/thumbs/")

        self._image_media = Media()
        self._image_media.path = "mediastack/tests/media/input/input_artist/cat_album/image_1.jpg"
        self._image_media.hash = "2550bc86af322d4e84e3c6a6480f8d4f"
        self._image_media.type = "image"

        self._gif_media = Media()
        self._gif_media.path = "mediastack/tests/media/input/input_artist/cat_album/image_2.gif"
        self._gif_media.hash = "f348d49188a34525ebdb3587a27eb9c5"
        self._gif_media.type = "animated_image"

        self._video_media = Media()
        self._video_media.path = "mediastack/tests/media/input/input_artist/cat_album/video_1.mp4"
        self._video_media.hash = "84648e4adbce47124bfea1348b9286ba"
        self._video_media.type = "video"

    @classmethod
    def tearDownClass(self):
        os.remove("mediastack/tests/media/output/thumbs/" + self._image_media.hash)
        os.remove("mediastack/tests/media/output/thumbs/" + self._gif_media.hash)
        os.remove("mediastack/tests/media/output/thumbs/" + self._video_media.hash)
        os.rmdir("mediastack/tests/media/output/thumbs")

    def test_create_thumbnail_from_image(self):
        self.assertTrue(self._thumbnailer.create_thumbnail(self._image_media))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/" + self._image_media.hash))
        self.assertEqual("abef4f46d31babd03b38cc9929779b66", MediaIO.hash_file("mediastack/tests/media/output/thumbs/" + self._image_media.hash))

    def test_create_thumbnail_from_gif(self):
        self.assertTrue(self._thumbnailer.create_thumbnail(self._gif_media))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/" + self._gif_media.hash))
        self.assertEqual("6ea27f44783d4bf8e024b1129473b872", MediaIO.hash_file("mediastack/tests/media/output/thumbs/" + self._gif_media.hash))

    def test_create_thumbnail_from_video(self):
        self.assertTrue(self._thumbnailer.create_thumbnail(self._video_media))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/" + self._video_media.hash))
        self.assertEqual("776022ffa742121f9be4b55993d2d6be", MediaIO.hash_file("mediastack/tests/media/output/thumbs/" + self._video_media.hash))
    
    def test_create_thumbnail_from_invalid_file(self):
        text_file = Media()
        text_file.path = "mediastack/tests/media/input/Text File.txt"
        text_file.hash = "ff275301eee9b114becf1e1089b8da4f"
        self.assertFalse(self._thumbnailer.create_thumbnail(text_file))

    def test_create_thumbnail_from_non_existant_file(self):
        some_file = Media()
        some_file.path = "mediastack/tests/media/input/doesnt exist"
        some_file.hash = "hash"
        self.assertFalse(self._thumbnailer.create_thumbnail(some_file))
    