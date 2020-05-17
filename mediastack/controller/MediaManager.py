import os, copy
import sqlalchemy as sa
from typing import List
from mediastack.model.Base import Base
from mediastack.model.Media import Media
from mediastack.model.Album import Album
from mediastack.model.Tag import Tag
from mediastack.utility.MediaIO import MediaIO
from mediastack.utility.MediaInitializer import MediaInitializer
from mediastack.utility.InputSanitizer import sanitize_input

class MediaManager:

    def __init__(self, session: sa.orm.Session):
        self._session = session

        self._media_initializer = MediaInitializer(self._session, MediaIO())
        self._media_initializer.initialize_media_from_disk();

    def find_media(self, media_hash: str) -> Media:
        if media_hash is None:
            return None;
        return self._session.query(Media).get(media_hash)

    def find_tag(self, tag_name: str) -> Tag:
        if tag_name is None:
            return None;
        return self._session.query(Tag).get(tag_name)

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

        if media.album is not None and tag in media.album.get_media_tags():
            media.album.tags.append(tag)
        
        self._write_media_changes(media)

        self._session.commit()

        return tag

    def remove_tag(self, media: Media, tag: Tag) -> Tag:
        if media is None or tag is None:
            return None
        
        if tag in media.tags:
            media.tags.remove(tag)
        if media.album is not None and tag not in media.album.get_media_tags():
            media.album.tags.remove(tag)
        self._write_media_changes(media)
        self._session.commit()
        return tag

    def change_source(self, media: Media, new_source: str) -> str:
        if media is None or new_source is None or len(new_source) == 0:
            return None
        
        media.source = new_source
        self._write_media_changes(media)
        self._session.commit()
        return new_source

    def change_score(self, media: Media, new_score: str) -> int:
        if media is None or new_score is None:
            return None
        try:
            new_score = int(new_score)
        except:
            raise ValueError("Invalid score.")

        if media.album_name is not None and media.album.cover == media:
            for album_media in media.album.media:
                album_media.score = new_score
                self._write_media_changes(media)
        else:
            media.score = new_score
            self._write_media_changes(media)
        self._session.commit()
        return new_score

#    def search(self, media_set: str, criteria: List[str] = []) -> List[Media]:
#        search_result = self._search_manager.search(self._session, self.find_media_set(media_set), criteria)
#        search_result.sort()
#        return search_result

#    def find_media_set(self, set_string: str) -> MediaSet:
#        if set_string is None:
#            return MediaSet.GENERAL
#        media_set = MediaSet(set_string.lower())
#        if media_set is None:
#            return MediaSet.GENERAL
#        return media_set
    
    def _write_media_changes(self, media: Media) -> None:
        #try:
        old_hash = copy.copy(media.hash)
        MediaIO().write_iptc_info_to_media(media)
        media.hash = MediaIO().hash_file(media.path)
        self._session.refresh(media)
        os.rename("thumbs/" + old_hash, "thumbs/" + media.hash)
        #except AttributeError:
            #print("Error writing changes to " + media.path)
    