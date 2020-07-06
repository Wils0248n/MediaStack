import os
import subprocess
from PIL import Image, UnidentifiedImageError
from mediastack.utility.MediaIO import MediaIO

class Thumbnailer:

    def __init__(self, thumbnail_directory, height: int = 175, width: int = 225):
        self.__thumbnail_directory = thumbnail_directory
        self.__height = height
        self.__width = width

        self._mediaio = MediaIO()
        self._create_thumbnail_directory()

    def _create_thumbnail_directory(self):
        try:
            os.mkdir(self.__thumbnail_directory)
        except FileExistsError:
            pass

    def create_thumbnail(self, media_path: str) -> bool:
        if media_path is None or not os.path.isfile(media_path):
            return False

        media_hash = self._mediaio.hash_file(media_path)
        if os.path.isfile(self.__thumbnail_directory + media_hash):
            return True

        media_type = self._mediaio.determine_media_type(media_path)
        if media_type == "image" or media_type == "animated_image":
            return self._create_image_thumbnail(media_path, media_hash)
        if media_type == "video":
            return self._create_video_thumbnail(media_path, media_hash)

    def _create_image_thumbnail(self, media_path: str, media_hash: str) -> bool:
        try:
            image = Image.open(media_path)
        except UnidentifiedImageError:
            return False
        image.thumbnail((self.__width, self.__height))
        output_path = self.__thumbnail_directory + media_hash
        image.save(output_path, format=image.format)
        return True

    def _create_video_thumbnail(self, media_path: str, media_hash: str) -> bool:
        output_path = self.__thumbnail_directory + media_hash
        size = str(self.__height) + "x" + str(self.__width)
        FNULL = open(os.devnull, 'w')
        return_code = subprocess.call(['ffmpeg', '-i', media_path, '-ss', '00:00:01.000',
            '-vframes', '1', '-s', size, '-f', 'image2', output_path], stdout=FNULL, stderr=subprocess.STDOUT)
        return return_code == 0
