import unittest
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag

class TestAlbumGetMediaTags(unittest.TestCase):
    def test_album_with_no_media(self):
        self.assertEqual([], Album("album").get_media_tags())

    def test_album_with_media_with_no_tags(self):
        album = Album("album")
        album.media.append(Media())
        self.assertEqual([], album.get_media_tags())

    def test_album_with_one_media_with_tags(self):
        album = Album("album")
        media = Media()
        tag1 = Tag("1")
        tag2 = Tag("2")
        media.tags.append(tag1)
        media.tags.append(tag2)
        album.media.append(media)
        self.assertEqual([tag1, tag2], album.get_media_tags())

    def test_album_with_multiple_media_with_duplicate_tags(self):
        album = Album("album")
        media1 = Media()
        media2 = Media()
        media3 = Media()
        tag1 = Tag("1")
        tag2 = Tag("2")
        tag3 = Tag("3")

        media1.tags.append(tag1)
        media1.tags.append(tag2)

        media2.tags.append(tag2)
        media2.tags.append(tag3)

        media3.tags.append(tag3)
        media3.tags.append(tag1)

        album.media.append(media1)
        album.media.append(media2)
        album.media.append(media3)

        expected = [tag1, tag2, tag3]
        result = album.get_media_tags()

        self.assertEqual(expected, result)
