import unittest, os, shutil, copy
import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.controller.MediaManager import MediaManager

class TestMediaManagerAddTag(unittest.TestCase):
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

    def test_add_new_tag_to_valid_media_not_in_album(self):
        media_manager = MediaManager(self._session)

        media = media_manager.find_media("d63f614e336fec57117d74b14aad1702")
        self.assertIsNotNone(media)
        new_tag = media_manager.create_tag("tag_name")
        self.assertIsNotNone(new_tag)

        originalMediaTags = copy.deepcopy(media.tags)
        originalTagMedia = copy.deepcopy(new_tag.media)

        self.assertFalse(new_tag in media.tags)
        self.assertFalse(media in new_tag.media)

        result = media_manager.add_tag(media, new_tag)
        self.assertEqual(new_tag, result)

        self.assertTrue(media in new_tag.media)
        self.assertTrue(new_tag in media.tags)

        for current_tag in originalMediaTags:
            self.assertTrue(current_tag in media.tags)

        for current_media in originalTagMedia:
            self.assertTrue(media in new_tag.media)

    def test_add_new_tag_to_valid_media_in_album(self):
        media_manager = MediaManager(self._session)

        media = media_manager.find_media("2550bc86af322d4e84e3c6a6480f8d4f")
        self.assertIsNotNone(media)
        new_tag = media_manager.create_tag("tag_name")
        self.assertIsNotNone(new_tag)

        originalMediaTags = copy.deepcopy(media.tags)
        originalTagMedia = copy.deepcopy(new_tag.media)
        originalAlbumTags = copy.deepcopy(media.album.tags)

        self.assertFalse(new_tag in media.tags)
        self.assertFalse(media in new_tag.media)

        result = media_manager.add_tag(media, new_tag)
        self.assertEqual(new_tag, result)

        self.assertTrue(media in new_tag.media)
        self.assertTrue(new_tag in media.tags)
        self.assertTrue(new_tag in media.album.tags)

        for current_tag in originalMediaTags:
            self.assertTrue(current_tag in media.tags)
        
        for current_tag in originalAlbumTags:
            self.assertTrue(current_tag in media.album.tags)

        for current_media in originalTagMedia:
            self.assertTrue(media in new_tag.media)
    
    def test_add_duplicate_tag_to_valid_media_not_in_album(self):
        media_manager = MediaManager(self._session)

        media = media_manager.find_media("d63f614e336fec57117d74b14aad1702")
        self.assertIsNotNone(media)
        existing_tag = media_manager.find_tag("dog")
        self.assertIsNotNone(existing_tag)

        originalMediaTags = copy.deepcopy(media.tags)
        originalTagMedia = copy.deepcopy(existing_tag.media)

        self.assertTrue(existing_tag in media.tags)
        self.assertTrue(media in existing_tag.media)

        result = media_manager.add_tag(media, existing_tag)
        self.assertIsNone(result)

        self.assertTrue(existing_tag in media.tags)
        self.assertTrue(media in existing_tag.media)

        for current_tag in originalMediaTags:
            self.assertTrue(current_tag in media.tags)

        for current_media in originalTagMedia:
            self.assertTrue(media in existing_tag.media)
    
    def test_add_duplicate_tag_to_valid_media_in_album(self):
        media_manager = MediaManager(self._session)

        media = media_manager.find_media("2550bc86af322d4e84e3c6a6480f8d4f")
        self.assertIsNotNone(media)
        existing_tag = media_manager.find_tag("dog")
        self.assertIsNotNone(existing_tag)
        self.assertIsNotNone(media_manager.add_tag(media, existing_tag))

        originalMediaTags = copy.deepcopy(media.tags)
        originalTagMedia = copy.deepcopy(existing_tag.media)
        originalAlbumTags = copy.deepcopy(media.album.tags)

        self.assertTrue(existing_tag in media.tags)
        self.assertTrue(media in existing_tag.media)

        result = media_manager.add_tag(media, existing_tag)
        self.assertIsNone(result)

        self.assertTrue(existing_tag in media.tags)
        self.assertTrue(media in existing_tag.media)
        self.assertTrue(existing_tag in media.album.tags)

        for current_tag in originalMediaTags:
            self.assertTrue(current_tag in media.tags)
        
        for current_tag in originalAlbumTags:
            self.assertTrue(current_tag in media.album.tags)

        for current_media in originalTagMedia:
            self.assertTrue(media in existing_tag.media)
    