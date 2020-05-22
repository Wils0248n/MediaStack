import unittest, os, shutil
import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.controller.MediaManager import MediaManager

class TestMediaManagerFindMedia(unittest.TestCase):
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
        self._engine = sa.create_engine('sqlite:///test.db', connect_args={'check_same_thread': False})
        Base.metadata.create_all(bind=self._engine)
        self._session_maker = sa.orm.sessionmaker(bind=self._engine)
        self._session = self._session_maker()

    @classmethod
    def tearDown(self):
        self._session.close()
        os.chdir("../..")
        #shutil.rmtree(self._media_directory)
        #shutil.rmtree(self._thumbnail_directory)

    def test_find_existing_media(self):
        media_manager = MediaManager(self._session)
        media = media_manager.find_media("2550bc86af322d4e84e3c6a6480f8d4f")
        self.assertIsNotNone(media)
        self.assertEqual("2550bc86af322d4e84e3c6a6480f8d4f", media.hash)
        self.assertEqual("media/input/input_artist/cat_album/image_1.jpg", media.path)
        self.assertEqual("input", media.category.name)
        self.assertEqual("input_artist", media.artist.name)
        self.assertEqual("cat_album", media.album.name)
        self.assertEqual("image", media.type)
        self.assertEqual(None, media.source)
        self.assertEqual(0, media.score)
    
    def test_find_non_existant_media(self):
        media_manager = MediaManager(self._session)
        media = media_manager.find_media("non_existant_media_hash")
        self.assertIsNone(media)

    def test_find_media_when_hash_is_none(self):
        media_manager = MediaManager(self._session)
        media = media_manager.find_media(None)
        self.assertIsNone(media)
    