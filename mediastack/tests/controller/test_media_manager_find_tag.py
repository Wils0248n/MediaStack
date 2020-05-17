import unittest, os, shutil
import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.controller.MediaManager import MediaManager

class TestMediaManagerFindTag(unittest.TestCase):
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

    @classmethod
    def tearDown(self):
        self._session.close()
        os.chdir("../..")
        shutil.rmtree(self._media_directory)
        shutil.rmtree(self._thumbnail_directory)

    def test_find_existing_tag(self):
        media_manager = MediaManager(self._session)
        tag = media_manager.find_tag("dog")

        self.assertIsNotNone(tag)
    
    def test_find_non_existant_tag(self):
        media_manager = MediaManager(self._session)
        tag = media_manager.find_tag("non_existant_tag")
        self.assertIsNone(tag)

    def test_find_none_tag(self):
        media_manager = MediaManager(self._session)
        tag = media_manager.find_tag(None)
        self.assertIsNone(tag)
    