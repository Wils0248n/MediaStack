import os, copy
import sqlalchemy as sa
from typing import List
from mediastack.model import *
from mediastack.utility.MediaIO import MediaIO

class MediaManager:

    def __init__(self, session: sa.orm.Session):
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

    def find_media(self, media_hash: str) -> Media:
        if media_hash is None:
            return None;
        return self._session.query(Media).get(media_hash)

    def find_tag(self, tag_name: str) -> Tag:
        if tag_name is None:
            return None;
        return self._session.query(Tag).get(tag_name)

    def find_album(self, album_name: str) -> Album:
        if album_name is None:
            return None
        return self._session.query(Album).get(album_name)

    def find_artist(self, artist_name: str) -> Artist:
        if artist_name is None:
            return None
        return self._session.query(Artist).get(artist_name)

    def find_category(self, category_name: str) -> Category:
        if category_name is None:
            return None
        return self._session.query(Category).get(category_name)

    def create_tag(self, tag_name: str) -> Tag:
        if self.find_tag(tag_name) is not None:
            return None
        tag = Tag(tag_name)
        self._session.add(tag)
        return tag

    def add_tag(self, media: Media, tag: Tag) -> Tag:
        if media is None or tag is None or tag in media.tags:
            return None

        media.tags.append(tag)
        
        self._update_tags_on_disk(media)
        self._session.commit()
        return tag

    def remove_tag(self, media: Media, tag: Tag) -> Tag:
        if media is None or tag is None or tag not in media.tags:
            return None
        
        if tag in media.tags:
            media.tags.remove(tag)
        else:
            return None

        self._update_tags_on_disk(media)
        self._session.commit()
        return tag

    def change_source(self, media: Media, new_source: str) -> str:
        if media is None or new_source is None or len(new_source) == 0:
            return None
        
        media.source = new_source
        self._update_source_on_disk(media)
        self._session.commit()
        return new_source

    def change_score(self, media: Media, new_score: str) -> int:
        if media is None or new_score is None:
            return None
        
        try:
            new_score = int(new_score)
        except:
            return None

        if media.album_name is not None and media.album.cover == media:
            for album_media in media.album.media:
                album_media.score = new_score
                self._update_score_on_disk(media)
        else:
            media.score = new_score
            self._update_score_on_disk(media)
        self._session.commit()
        return new_score
    
    def get_next_media_in_album(self, media: Media) -> Media:
        if media.album is None:
            return None
        current_index = media.album.media.index(media)
        if current_index == len(media.album.media) - 1:
            return media.album.media[0]
        return media.album.media[current_index + 1]

    def get_previous_media_in_album(self, media: Media) -> Media:
        if media.album is None:
            return None
        current_index = media.album.media.index(media)
        if current_index == 0:
            return media.album.media[len(media.album.media) - 1]
        return media.album.media[current_index - 1]

    def _update_score_on_disk(self, media: Media) -> None:
        old_hash = copy.copy(media.hash)
        MediaIO().write_score_to_file(media.path, media.score)
        media.hash = MediaIO().hash_file(media.path)
        self._session.refresh(media)
        os.rename("thumbs/" + old_hash, "thumbs/" + media.hash)
    
    def _update_source_on_disk(self, media: Media) -> None:
        old_hash = copy.copy(media.hash)
        MediaIO().write_score_to_file(media.path, media.source)
        media.hash = MediaIO().hash_file(media.path)
        self._session.refresh(media)
        os.rename("thumbs/" + old_hash, "thumbs/" + media.hash)

    def _update_tags_on_disk(self, media: Media) -> None:
        old_hash = copy.copy(media.hash)
        MediaIO().write_tags_to_file(media.path, [tag.name for tag in media.tags])
        media.hash = MediaIO().hash_file(media.path)
        self._session.refresh(media)
        os.rename("thumbs/" + old_hash, "thumbs/" + media.hash)
