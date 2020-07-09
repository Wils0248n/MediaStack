import os, copy
import sqlalchemy as sa
from typing import List
from mediastack.model import *
from mediastack.utility.MediaIO import MediaIO

class MediaManager:

    def __init__(self, session: sa.orm.Session, write_metadata: bool = False):
        self._write_metadata = write_metadata
        self._session = session

    def get_media(self) -> List[Media]:
        return list(self._session.query(Media))

    def get_albums(self) -> List[Album]:
        return list(self._session.query(Album))

    def get_tags(self) -> List[Tag]:
        return list(self._session.query(Tag))

    def get_artists(self) -> List[Artist]:
        return list(self._session.query(Artist))

    def get_categories(self) -> List[Category]:
        return list(self._session.query(Category))

    def find_media_by_id(self, media_id: int) -> Media:
        if media_id is None:
            return None
        return self._session.query(Media).get(media_id)

    def find_media_by_hash(self, media_hash: str) -> Media:
        if media_hash is None:
            return None
        return self._session.query(Media).filter(Media.hash == media_hash).first()

    def find_media_by_path(self, media_path: str) -> Media:
        if media_path is None:
            return None
        return self._session.query(Media).filter(Media.path == media_path).first()

    def find_tag_by_id(self, tag_id: int) -> Tag:
        if tag_id is None:
            return None
        return self._session.query(Tag).get(tag_id)

    def find_tag_by_name(self, tag_name: str) -> Tag:
        if tag_name is None:
            return None
        return self._session.query(Tag).filter(Tag.name == tag_name).first()

    def find_album_by_id(self, album_id: int) -> Album:
        if album_id is None:
            return None
        return self._session.query(Album).get(album_id)

    def find_artist_by_id(self, artist_id: int) -> Artist:
        if artist_id is None:
            return None
        return self._session.query(Artist).get(artist_id)

    def find_artist_by_name(self, artist_name: str) -> Artist:
        if artist_name is None:
            return None
        return self._session.query(Artist).filter(Artist.name == artist_name).first()

    def find_category_by_id(self, category_id: int) -> Category:
        if category_id is None:
            return None
        return self._session.query(Category).get(category_id)

    def find_category_by_name(self, category_name: str) -> Category:
        if category_name is None:
            return None
        return self._session.query(Category).filter(Category.name == category_name).first()

    def create_media(self, hash: str, path: str, type: str, source: str = None, score: int = 0, category: str = None, artist: str = None, album: str = None, tags: List[str] = []) -> Media:
        if hash is None or path is None:
            return None

        media = self.find_media_by_hash(hash)
        
        if media is None:
            media = Media()
            media.hash = hash
            self._session.add(media)
        elif media.path is not None and os.path.isfile(media.path) and MediaIO.hash_file(media.path) == media.hash:
            return None
        
        media.path = path
        media.type = type
        media.source = source
        media.score = score
        media.category = self.create_category(category)
        media.artist = self.create_artist(artist)
        media.album = self.create_album(album, media.category, media.artist)

        for tag_name in tags:
            media.tags.append(self._create_tag(tag_name))

        if media.album is not None:
            media.album.tags = media.album.get_media_tags()

        self._session.commit()
        return media

    def create_album(self, album_name: str, category: Category, artist: Artist) -> Album:
        if album_name is None or category is None or artist is None:
            return None

        for album in artist.albums:
            if album.name == album_name:
                return album

        album = Album(album_name)
        album.category = category
        album.artist = artist
        self._session.add(album)
        self._session.commit()
        return album

    def create_artist(self, artist_name: str) -> Artist:
        if artist_name is None:
            return None
        potential_existing_artist = self.find_artist_by_name(artist_name)
        if potential_existing_artist is not None:
            return potential_existing_artist
        artist = Artist(artist_name)
        self._session.add(artist)
        self._session.commit()
        return artist

    def create_category(self, category_name: str) -> Category:
        if category_name is None:
            return None
        potential_existing_category = self.find_category_by_name(category_name)
        if potential_existing_category is not None:
            return potential_existing_category
        category = Category(category_name)
        self._session.add(category)
        self._session.commit()
        return category

    def _create_tag(self, tag_name: str) -> Tag:
        if tag_name is None:
            return None

        tag_name = tag_name.lower()

        potential_existing_tag = self.find_tag_by_name(tag_name)
        if potential_existing_tag is not None:
            return potential_existing_tag
        
        tag = Tag(tag_name)
        self._session.add(tag)
        return tag

    def create_tag(self, tag_name: str) -> Tag:
        tag = self._create_tag(tag_name)
        if tag is not None:
            self._session.commit()
        return tag

    def add_tag_to_media(self, media: Media, tag: Tag) -> Tag:
        if media is None or tag is None or tag in media.tags:
            return None

        media.tags.append(tag)

        if media.album_id is not None:
            media.album.tags = media.album.get_media_tags()
        
        self._session.commit()
        self._write_metadata_to_disk(media)
        return tag

    def remove_tag_from_media(self, media: Media, tag: Tag) -> Tag:
        if media is None or tag is None or tag not in media.tags:
            return None
        
        media.tags.remove(tag)

        if media.album_id is not None:
            media.album.tags = media.album.get_media_tags()

        self._session.commit()
        self._write_metadata_to_disk(media)
        return tag

    def change_media_tags(self, media: Media, tags: List[Tag]) -> Media:
        media.tags = tags

        if media.album_id is not None:
            media.album.tags = media.album.get_media_tags()

        self._session.commit()
        self._write_metadata_to_disk(media)
            
    def change_media_source(self, media: Media, new_source: str) -> str:
        if media is None or new_source is None or len(new_source) == 0:
            return None
        
        media.source = new_source
        self._session.commit()
        self._write_metadata_to_disk(media)
        return new_source

    def change_media_score(self, media: Media, new_score: str) -> int:
        if media is None or new_score is None:
            return None
        
        try:
            new_score = int(new_score)
        except:
            return None

        media.score = new_score
        self._session.commit()
        self._write_metadata_to_disk(media)

        return new_score
    
    def disable_media(self, media: Media) -> None:
        media.path = None
        media.category = None
        media.artist = None

        album = media.album

        media.album = None

        if album is not None:
            if len(album.media) == 0:
                self._session.delete(album)
            else:
                album.tags = album.get_media_tags()

        self._session.commit()
    
    def _write_metadata_to_disk(self, media: Media) -> None:
        if not self._write_metadata:
            return

        if media.type != "image":
            return
        try:
            MediaIO().write_metadata_to_file(media.path, media.tags, media.source, media.score)
        except AttributeError:
            return
        new_hash = MediaIO().hash_file(media.path)
        if new_hash != media.hash:
            os.rename("thumbs/" + media.hash, "thumbs/" + new_hash)
            media.hash = new_hash
            self._session.commit()
