import unittest, os, shutil
import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.model.Media import Media
from mediastack.model.Tag import Tag
from mediastack.model.Album import Album
from mediastack.model.Artist import Artist
from mediastack.model.Category import Category
from mediastack.utility.MediaIO import MediaIO
from mediastack.controller.MediaInitializer import MediaInitializer
from mediastack.controller.MediaManager import MediaManager

class TestMediaInitializerInitializeMedia(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._previous_cwd = os.getcwd()
        os.chdir("mediastack/tests/")

        self._media_directory = "media/output/media/"
        self._thumbnail_directory = "media/output/thumbs/"

    @classmethod
    def tearDownClass(self):
        os.chdir(self._previous_cwd)

    @classmethod
    def setUp(self):
        os.mkdir(self._media_directory)
        os.mkdir(self._thumbnail_directory)

        shutil.copytree("media/input", self._media_directory + "input")

        os.chdir("media/output")
        self._engine = sa.create_engine('sqlite://', connect_args={'check_same_thread': False})
        Base.metadata.create_all(bind=self._engine)
        self._session_maker = sa.orm.sessionmaker(bind=self._engine)
        self._session = self._session_maker()
        self._media_initializer = MediaInitializer(MediaManager(self._session))

    @classmethod
    def tearDown(self):
        self._session.close()
        os.chdir("../..")
        shutil.rmtree(self._media_directory)
        shutil.rmtree(self._thumbnail_directory)

    def test_initialize_media(self):
        os.remove("media/input/input_artist/cat_album/image_2.gif")
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(3, len(list(self._session.query(Media).filter(Media.path != None))))

        image_1 = self._session.query(Media).get("2550bc86af322d4e84e3c6a6480f8d4f")
        self.assertIsNotNone(image_1)
        self.assertEqual("2550bc86af322d4e84e3c6a6480f8d4f", image_1.hash)
        self.assertEqual("media/input/input_artist/cat_album/image_1.jpg", image_1.path)
        self.assertEqual("input", image_1.category.name)
        self.assertEqual("input_artist", image_1.artist.name)
        self.assertEqual("cat_album", image_1.album.name)
        self.assertEqual("image", image_1.type)
        self.assertEqual(None, image_1.source)
        self.assertEqual(0, image_1.score)

        image_3 = self._session.query(Media).get("d63f614e336fec57117d74b14aad1702")
        self.assertIsNotNone(image_3)
        self.assertEqual("d63f614e336fec57117d74b14aad1702", image_3.hash)
        self.assertEqual("media/input/input_artist/image_3.jpg", image_3.path)
        self.assertEqual("input", image_3.category.name)
        self.assertEqual("input_artist", image_3.artist.name)
        self.assertEqual(None, image_3.album)
        self.assertEqual("image", image_3.type)
        self.assertEqual("google", image_3.source)
        self.assertEqual(2, image_3.score)

        video_1 = self._session.query(Media).get("84648e4adbce47124bfea1348b9286ba")
        self.assertIsNotNone(video_1)
        self.assertEqual("84648e4adbce47124bfea1348b9286ba", video_1.hash)
        self.assertEqual("media/input/input_artist/cat_album/video_1.mp4", video_1.path)
        self.assertEqual("input", video_1.category.name)
        self.assertEqual("input_artist", video_1.artist.name)
        self.assertEqual("cat_album", video_1.album.name)
        self.assertEqual("video", video_1.type)
        self.assertEqual(None, video_1.source)
        self.assertEqual(0, video_1.score)
    
    def test_initialize_new_media(self):
        os.remove("media/input/input_artist/cat_album/image_2.gif")
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(3, len(list(self._session.query(Media).filter(Media.path != None))))
        shutil.copyfile("../input/input_artist/cat_album/image_2.gif", "media/input/input_artist/cat_album/image_2.gif")
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))

    def test_remove_missing_media(self):
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        os.remove("media/input/input_artist/cat_album/image_2.gif")
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(3, len(list(self._session.query(Media).filter(Media.path != None))))

    def test_moved_media_from_album(self):
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(4, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(3, len(list(self._session.query(Album).get("cat_album").media)))
        
        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist/cat_album/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist", image_2.artist.name)
        self.assertEqual("cat_album", image_2.album.name)

        shutil.copy("media/input/input_artist/cat_album/image_2.gif", "media/input/input_artist/image_2.gif")
        os.remove("media/input/input_artist/cat_album/image_2.gif")

        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(4, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(2, len(list(self._session.query(Album).get("cat_album").media)))

        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist", image_2.artist.name)
        self.assertEqual(None, image_2.album)

    def test_moved_media_from_artist(self):
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(4, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(3, len(list(self._session.query(Album).get("cat_album").media)))
        
        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist/cat_album/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist", image_2.artist.name)
        self.assertEqual("cat_album", image_2.album.name)

        shutil.copy("media/input/input_artist/cat_album/image_2.gif", "media/input/image_2.gif")
        os.remove("media/input/input_artist/cat_album/image_2.gif")

        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(3, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(2, len(list(self._session.query(Album).get("cat_album").media)))

        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual(None, image_2.artist)
        self.assertEqual(None, image_2.album)

    def test_moved_media_from_category(self):
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(4, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(3, len(list(self._session.query(Album).get("cat_album").media)))
        
        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist/cat_album/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist", image_2.artist.name)
        self.assertEqual("cat_album", image_2.album.name)

        shutil.copy("media/input/input_artist/cat_album/image_2.gif", "media/image_2.gif")
        os.remove("media/input/input_artist/cat_album/image_2.gif")

        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(3, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(3, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(2, len(list(self._session.query(Album).get("cat_album").media)))

        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/image_2.gif", image_2.path)
        self.assertEqual(None, image_2.category)
        self.assertEqual(None, image_2.artist)
        self.assertEqual(None, image_2.album)
    
    def test_moved_media_to_another_album(self):
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(4, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(3, len(list(self._session.query(Album).get("cat_album").media)))
        
        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist/cat_album/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist", image_2.artist.name)
        self.assertEqual("cat_album", image_2.album.name)

        os.mkdir("media/input/input_artist/cat_album2")
        shutil.copy("media/input/input_artist/cat_album/image_2.gif", "media/input/input_artist/cat_album2/image_2.gif")
        os.remove("media/input/input_artist/cat_album/image_2.gif")

        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(4, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(2, len(list(self._session.query(Album).get("cat_album").media)))
        self.assertEquals(1, len(list(self._session.query(Album).get("cat_album2").media)))

        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist/cat_album2/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist", image_2.artist.name)
        self.assertEqual("cat_album2", image_2.album.name)

    def test_moved_media_to_another_album_and_another_artist(self):
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(4, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(3, len(list(self._session.query(Album).get("cat_album").media)))
        
        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist/cat_album/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist", image_2.artist.name)
        self.assertEqual("cat_album", image_2.album.name)

        os.mkdir("media/input/input_artist2")
        os.mkdir("media/input/input_artist2/cat_album2")
        shutil.copy("media/input/input_artist/cat_album/image_2.gif", "media/input/input_artist2/cat_album2/image_2.gif")
        os.remove("media/input/input_artist/cat_album/image_2.gif")

        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(3, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(2, len(list(self._session.query(Album).get("cat_album").media)))
        self.assertEquals(1, len(list(self._session.query(Artist).get("input_artist2").media)))
        self.assertEquals(1, len(list(self._session.query(Album).get("cat_album2").media)))

        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist2/cat_album2/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist2", image_2.artist.name)
        self.assertEqual("cat_album2", image_2.album.name)

    def test_moved_media_to_another_album_and_another_artist_and_another_category(self):
        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(4, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(4, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(3, len(list(self._session.query(Album).get("cat_album").media)))
        
        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input/input_artist/cat_album/image_2.gif", image_2.path)
        self.assertEqual("input", image_2.category.name)
        self.assertEqual("input_artist", image_2.artist.name)
        self.assertEqual("cat_album", image_2.album.name)

        os.mkdir("media/input2")
        os.mkdir("media/input2/input_artist2")
        os.mkdir("media/input2/input_artist2/cat_album2")
        shutil.copy("media/input/input_artist/cat_album/image_2.gif", "media/input2/input_artist2/cat_album2/image_2.gif")
        os.remove("media/input/input_artist/cat_album/image_2.gif")

        self._media_initializer.initialize_media_from_disk()
        self.assertEquals(4, len(list(self._session.query(Media).filter(Media.path != None))))
        self.assertEquals(3, len(list(self._session.query(Category).get("input").media)))
        self.assertEquals(3, len(list(self._session.query(Artist).get("input_artist").media)))
        self.assertEquals(2, len(list(self._session.query(Album).get("cat_album").media)))
        self.assertEquals(1, len(list(self._session.query(Category).get("input2").media)))
        self.assertEquals(1, len(list(self._session.query(Artist).get("input_artist2").media)))
        self.assertEquals(1, len(list(self._session.query(Album).get("cat_album2").media)))

        image_2 = self._session.query(Media).get("f348d49188a34525ebdb3587a27eb9c5")
        self.assertIsNotNone(image_2)
        self.assertEqual("f348d49188a34525ebdb3587a27eb9c5", image_2.hash)
        self.assertEqual("media/input2/input_artist2/cat_album2/image_2.gif", image_2.path)
        self.assertEqual("input2", image_2.category.name)
        self.assertEqual("input_artist2", image_2.artist.name)
        self.assertEqual("cat_album2", image_2.album.name)