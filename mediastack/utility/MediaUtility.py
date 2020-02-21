import os
import hashlib
import filetype
import logging
from typing import List, Dict
from iptcinfo3 import IPTCInfo
from model.MediaType import MediaType

logging.getLogger('iptcinfo').setLevel(logging.ERROR)

def hash_file(file_path: str) -> str:
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buffer = file.read()
        hasher.update(buffer)
    return hasher.hexdigest()

def extract_media_meta(media_path: str) -> Dict[str, str]:
    media_meta = {}
    try:
        media_meta["category"] = media_path.split(os.path.sep)[1]
    except:
        media_meta["category"] = None

    try:
        media_meta["artist"] = media_path.split(os.path.sep)[2]
    except:
        media_meta["artist"] = None

    try:
        album_path = os.path.sep.join(media_path.split(os.path.sep)[:-1])
        album_name = media_path.split(os.path.sep)[3]
        if album_path + os.path.sep + album_name == media_path:
            media_meta["album"] = None
        else:
            media_meta["album"] = album_name
    except:
        media_meta["album"] = None
    
    return media_meta

def extract_keywords(media_path: str) -> List[str]:
    info = IPTCInfo(media_path)
    keywords = []
    for keyword in info['keywords']:
        keywords.append(keyword.decode("utf-8").replace(" ", "_").lower())
    return keywords

def extract_source(media_path: str) -> str:
    source = IPTCInfo(media_path)['caption/abstract']
    if source is not None:
        return source.decode("utf-8")
    else:
        return None

def determine_media_type(media_path: str) -> MediaType:
    file_type = filetype.guess(media_path)
    if file_type is not None:
        file_type = file_type.extension
        if file_type == "jpg" or file_type == "png":
            return MediaType.IMAGE
        if file_type == "gif":
            return MediaType.ANIMATED_IMAGE
        if file_type == "mp4" or file_type == "webm":
            return MediaType.VIDEO
    return None

def scan_directory(directory_path: str) -> List[str]:
    media_file_paths = []
    for currentDirectory, directories, files in os.walk(directory_path):
        for file in files:
            media_file_paths.append(os.path.join(currentDirectory, file))
    return media_file_paths