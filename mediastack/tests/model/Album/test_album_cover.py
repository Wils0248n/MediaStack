import unittest
from mediastack.model.Media import Media
from mediastack.model.Album import Album

class TestAlbumCover(unittest.TestCase):
    def test_album_cover_with_album_of_size_one(self):
        media = Media()
        media.hash = "hash"

        album = Album("album")
        album.media.append(media)

        self.assertEqual(media, album.cover)

    def test_album_cover_with_album_of_size_three(self):
        media1 = Media()
        media1.path = "3"
        media1.hash = "hash1"

        media2 = Media()
        media2.path = "2"
        media2.hash = "hash2"

        media3 = Media()
        media3.path = "1"
        media3.hash = "hash3"

        album = Album("album")
        album.media.append(media1)
        album.media.append(media2)
        album.media.append(media3)

        self.assertEqual(media3, album.cover)

    def test_album_with_no_media(self):
        self.assertIsNone(Album("album").cover)
    