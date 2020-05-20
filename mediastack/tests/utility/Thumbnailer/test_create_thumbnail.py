import unittest, os, shutil
import sqlalchemy as sa
from mediastack.utility.MediaIO import MediaIO
from mediastack.utility.Thumbnailer import Thumbnailer

class TestThumbnailerCreateThumbnail(unittest.TestCase):

    @classmethod
    def setUp(self):
        self._thumbnailer = Thumbnailer("mediastack/tests/media/output/thumbs/")

    @classmethod
    def tearDown(self):
        shutil.rmtree("mediastack/tests/media/output/thumbs")

    def test_create_thumbnail_from_image(self):
        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/image_1.jpg"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/2550bc86af322d4e84e3c6a6480f8d4f"))
        self.assertEqual("abef4f46d31babd03b38cc9929779b66", MediaIO.hash_file("mediastack/tests/media/output/thumbs/2550bc86af322d4e84e3c6a6480f8d4f"))

    def test_create_thumbnail_from_gif(self):
        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/image_2.gif"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/f348d49188a34525ebdb3587a27eb9c5"))
        self.assertEqual("6ea27f44783d4bf8e024b1129473b872", MediaIO.hash_file("mediastack/tests/media/output/thumbs/f348d49188a34525ebdb3587a27eb9c5"))

    def test_create_thumbnail_from_video(self):
        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/video_1.mp4"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/84648e4adbce47124bfea1348b9286ba"))
        self.assertEqual("776022ffa742121f9be4b55993d2d6be", MediaIO.hash_file("mediastack/tests/media/output/thumbs/84648e4adbce47124bfea1348b9286ba"))
    
    def test_create_image_thumbnail_twice(self):
        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/image_1.jpg"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/2550bc86af322d4e84e3c6a6480f8d4f"))
        self.assertEqual("abef4f46d31babd03b38cc9929779b66", MediaIO.hash_file("mediastack/tests/media/output/thumbs/2550bc86af322d4e84e3c6a6480f8d4f"))

        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/image_1.jpg"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/2550bc86af322d4e84e3c6a6480f8d4f"))
        self.assertEqual("abef4f46d31babd03b38cc9929779b66", MediaIO.hash_file("mediastack/tests/media/output/thumbs/2550bc86af322d4e84e3c6a6480f8d4f"))

    def test_create_gif_thumbnail_twice(self):
        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/image_2.gif"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/f348d49188a34525ebdb3587a27eb9c5"))
        self.assertEqual("6ea27f44783d4bf8e024b1129473b872", MediaIO.hash_file("mediastack/tests/media/output/thumbs/f348d49188a34525ebdb3587a27eb9c5"))

        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/image_2.gif"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/f348d49188a34525ebdb3587a27eb9c5"))
        self.assertEqual("6ea27f44783d4bf8e024b1129473b872", MediaIO.hash_file("mediastack/tests/media/output/thumbs/f348d49188a34525ebdb3587a27eb9c5"))

    def test_create_video_thumbnail_twice(self):
        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/video_1.mp4"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/84648e4adbce47124bfea1348b9286ba"))
        self.assertEqual("776022ffa742121f9be4b55993d2d6be", MediaIO.hash_file("mediastack/tests/media/output/thumbs/84648e4adbce47124bfea1348b9286ba"))

        self.assertTrue(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/input_artist/cat_album/video_1.mp4"))
        self.assertTrue(os.path.isfile("mediastack/tests/media/output/thumbs/84648e4adbce47124bfea1348b9286ba"))
        self.assertEqual("776022ffa742121f9be4b55993d2d6be", MediaIO.hash_file("mediastack/tests/media/output/thumbs/84648e4adbce47124bfea1348b9286ba"))

    def test_create_thumbnail_from_invalid_file(self):
        self.assertFalse(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/Text File.txt"))

    def test_create_thumbnail_from_non_existant_file(self):
        self.assertFalse(self._thumbnailer.create_thumbnail("mediastack/tests/media/input/doesnt exist"))
    