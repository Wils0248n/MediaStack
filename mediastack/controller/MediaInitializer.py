import os
from typing import List, Dict
from mediastack.model.Media import Media
from mediastack.controller.MediaManager import MediaManager
from mediastack.utility.Thumbnailer import Thumbnailer
from mediastack.utility.MediaIO import MediaIO

class MediaInitializer:
    def __init__(self, media_manager: MediaManager, media_dir: str = "media/", thumbnail_dir: str = "thumbs/"):
        self._media_manager = media_manager
        self.media_directory = media_dir
        self.thumbnail_directory = thumbnail_dir

        self._mediaio = MediaIO()
        self._thumbnailer = Thumbnailer(self.thumbnail_directory)

    def initialize_media_from_disk(self):
        #print("Scanning disk...")
        media_paths = MediaIO.scan_directory(self.media_directory)
        #print("Disabling missing Media...")
        self._find_and_disable_missing_media(media_paths)
        #print("Initializing new Media on Disk...")
        self._find_and_handle_new_media(media_paths)

    def _find_and_disable_missing_media(self, media_paths):
        #missing_media = 0
        for media in self._media_manager.get_media():
            if media.path not in media_paths:
                #missing_media += 1
                self._media_manager.disable_media(media)
        #print(str(missing_media) + " missing media found.")

    def _find_and_handle_new_media(self, media_paths: List[str]):
        mutated_media = self._find_mutated_media(media_paths)
        #print(str(len(mutated_media.keys())) + " new media found.")
        for media_file_hash in mutated_media.keys():
            media = self._media_manager.find_media(media_file_hash)
            if media is not None:
                #print("Reinitializing media: " + mutated_media[media_file_hash])
                media.path = mutated_media[media_file_hash]
                self._reinitialize_media_references(media)
            else:
                #print("Creating media: " + mutated_media[media_file_hash])
                self._media_manager.create_media(self.create_media(mutated_media[media_file_hash]))
                
    def _find_mutated_media(self, media_paths: List[str]) -> Dict[str, str]:
        mutated_media = {}
        for media_file_path in media_paths:
            potential_media = self._media_manager.find_media_by_path(media_file_path)
            if potential_media is None:
                mutated_media[MediaIO.hash_file(media_file_path)] = media_file_path
            elif potential_media.hash != MediaIO.hash_file(media_file_path):
                mutated_media[potential_media.hash] = media_file_path
        return mutated_media

    def create_media(self, media_path: str) -> Media:
        if not self._thumbnailer.create_thumbnail(media_path):
            #print("Failed to thumbnail: " + media_path)
            return None
        
        media_metadata = self._mediaio.extract_metadata_from_media_file(media_path)

        if media_metadata is None:
            #print("Couldn't initialize: " + media_path)
            return None

        media = Media()
        
        media.path = media_path
        media.type = media_metadata["type"]
        media.hash = media_metadata["hash"]
        media.source = media_metadata["source"]
        media.score = media_metadata["score"]

        self._initialize_media_references(media, media_metadata)

        for tag_name in media_metadata["tags"]:
            current_tag = self._media_manager.create_tag(tag_name)
            media.tags.append(current_tag)
            if media.album is not None and current_tag not in media.album.tags:
                media.album.tags.append(current_tag)
            
        return media

    def _initialize_media_references(self, media: Media, media_metadata: Dict):
        if media is None or media_metadata is None:
            return
        media_category = self._media_manager.create_category(media_metadata["category"])
        if media_category is not None:
            media_category.media.append(media)
        
        media_artist = self._media_manager.create_artist(media_metadata["artist"])
        if media_artist is not None:
            media_artist.media.append(media)
        
        media_album = self._media_manager.create_album(media_metadata["album"])
        if media_album is not None:
            media_album.media.append(media)
    
    def _reinitialize_media_references(self, media: Media) -> None:
        if media.artist_name is not None:
            media.artist.media.remove(media)
        if media.album_name is not None:
            media.album.media.remove(media)
        if media.category_name is not None:
            media.category.media.remove(media)
        
        self._initialize_media_references(media, self._mediaio.extract_metadata_from_media_file(media.path))
        self._media_manager._session.commit()
    