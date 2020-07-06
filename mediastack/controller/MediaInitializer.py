import os
from typing import List, Dict
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
        media_paths = MediaIO.scan_directory(self.media_directory)
        print("Disabling missing Media...")
        self._find_and_disable_missing_media(media_paths)
        print("Initializing new Media on Disk...")
        self._find_and_handle_new_media(media_paths)

    def _find_and_disable_missing_media(self, media_paths):
        missing_media = 0
        for media in self._media_manager.get_media():
            if media.path not in media_paths:
                missing_media += 1
                self._media_manager.disable_media(media)
        print(str(missing_media) + " missing media found.")

    def _find_and_handle_new_media(self, media_paths: List[str]):
        mutated_media = self._find_mutated_media(media_paths)
        print(str(len(mutated_media.keys())) + " new media found.")
        for media_file_hash in mutated_media.keys():
            self._create_media(self._create_media(mutated_media[media_file_hash]))
                
    def _find_mutated_media(self, media_paths: List[str]) -> Dict[str, str]:
        mutated_media = {}
        for media_file_path in media_paths:
            potential_media = self._media_manager.find_media_by_path(media_file_path)
            if potential_media is None:
                mutated_media[MediaIO.hash_file(media_file_path)] = media_file_path
            elif potential_media.hash != MediaIO.hash_file(media_file_path):
                mutated_media[potential_media.hash] = media_file_path
        return mutated_media

    def _create_media(self, media_path: str) -> None:
        if media_path is None:
            return None
        
        if not self._thumbnailer.create_thumbnail(media_path):
            print("Failed to thumbnail: " + media_path)
            return None
        try:
            media_metadata = self._mediaio.extract_metadata_from_media_file(media_path)
        except UnicodeDecodeError:
            return None

        if media_metadata is None:
            print("Couldn't read file: " + media_path)
            return None

        if self._media_manager.create_media(
            media_metadata['hash'],
            media_path,
            media_metadata["type"],
            media_metadata["source"],
            media_metadata["score"],
            media_metadata["category"],
            media_metadata["artist"],
            media_metadata["album"],
            media_metadata["tags"]
        ) is None:
            print("Duplicate File: {}".format(media_path))
    