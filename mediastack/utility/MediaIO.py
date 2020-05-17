import os, hashlib, filetype, logging, copy
from typing import List, Dict
from iptcinfo3 import IPTCInfo
from PIL import Image
from mediastack.utility.InputSanitizer import sanitize_input

logging.getLogger('iptcinfo').setLevel(logging.ERROR)

class MediaIO:

    def extract_metadata_from_media_file(self, media_path: str) -> Dict:
        if media_path is None or not os.path.isfile(media_path):
            return None

        media_metadata = {"score":0, "tags":[], "source":None}

        media_metadata["type"] = self._determine_media_type(media_path)

        if media_metadata["type"] is None:
            return None

        path_split = media_path.split(os.path.sep)

        media_metadata["category"] = path_split[1].lower() if 1 < len(path_split) \
            and os.path.isdir(os.sep.join([path_split[0], path_split[1]])) else None
        media_metadata["artist"] = path_split[2].lower() if 2 < len(path_split) \
            and os.path.isdir(os.sep.join([path_split[0], path_split[1], path_split[2]])) else None
        media_metadata["album"] = path_split[3].lower() if 3 < len(path_split) \
            and os.path.isdir(os.sep.join([path_split[0], path_split[1], path_split[2], path_split[3]])) else None

        if media_metadata["type"] == "image":
            iptc_info = IPTCInfo(media_path)

            media_metadata["tags"] = self._extract_keywords(iptc_info)
            media_metadata["source"] = self._extract_source(iptc_info)
            media_metadata["score"] = self._extract_score(iptc_info)

        media_metadata["hash"] = MediaIO.hash_file(media_path)
        
        return media_metadata

    def _determine_media_type(self, media_path: str) -> str:
        file_type = filetype.guess(media_path)
        if file_type is not None:
            file_type = file_type.extension
            if file_type == "jpg" or file_type == "png":
                return "image"
            if file_type == "gif":
                return "animated_image"
            if file_type == "mp4" or file_type == "webm":
                return "video"
        return None

    def _extract_keywords(self, iptc_info: IPTCInfo) -> List[str]:
        keywords = []
        for keyword in iptc_info['keywords']:
            keywords.append(sanitize_input(keyword.decode("utf-8")))
        return keywords

    def _extract_source(self, iptc_info: IPTCInfo) -> str:
        source = iptc_info['source']
        if source is not None:
            return source.decode("utf-8")
        else:
            source = iptc_info['caption/abstract']
            if source is not None:
                return source.decode("utf-8")
            else:
                return None

    def _extract_score(self, iptc_info: IPTCInfo) -> int:
        score = iptc_info['urgency']
        if score is not None:
            score = int(score.decode("utf-8"))
            return score
        return 0

    def strip_metadata(self, media_path: str):
        image = Image.open(media_path)

        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)

        image_without_exif.save(media_path, format=image.format)

    def write_iptc_info_to_media(self, media):
        if media is None or media.path is None or media.hash is None:
            return

        info = IPTCInfo(media.path)
        if media.source is not None:
            info['source'] = media.source
        if media.tags is not None and len(media.tags) > 0:
            tags = [tag.name for tag in media.tags]
            info['keywords'] = [tag_name.encode() for tag_name in tags]
        if media.score is not None:
            info['urgency'] = str(media.score)
        info.save()
        os.remove(media.path + '~')

    @staticmethod
    def hash_file(file_path: str) -> str:
        hasher = hashlib.md5()
        with open(file_path, 'rb') as file:
            buffer = file.read()
            hasher.update(buffer)
        return hasher.hexdigest()

    @staticmethod
    def scan_directory(directory_path: str) -> List[str]:
        if not (os.path.isdir(directory_path)):
            raise FileNotFoundError
        media_file_paths = []
        for currentDirectory, directories, files in os.walk(directory_path):
            for file in files:
                media_file_paths.append(os.path.join(currentDirectory, file))
        return media_file_paths
