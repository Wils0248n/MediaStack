import os
import subprocess
from PIL import Image, UnidentifiedImageError
from mediastack.model.Media import Media


class Thumbnailer:

    def __init__(self, thumbnail_directory, height: int = 175, width: int = 225):
        self.__thumbnail_directory = thumbnail_directory
        self._create_thumbnail_directory()
        self.__height = height
        self.__width = width

    def create_thumbnail(self, media: Media) -> bool:
        if os.path.isfile(self.__thumbnail_directory + media.hash):
            return True

        if media.type == "image":
            return self._create_image_thumbnail(media)
        if media.type == "animated_image":
            return self._create_image_thumbnail(media)
        if media.type == "video":
            return self._create_video_thumbnail(media)

    def _create_thumbnail_directory(self):
        try:
            os.mkdir(self.__thumbnail_directory)
        except FileExistsError:
            pass

    def _create_image_thumbnail(self, media_image: Media) -> bool:
        try:
            image = Image.open(media_image.path)
        except UnidentifiedImageError:
            return False
        image.thumbnail((self.__width, self.__height))
        output_path = self.__thumbnail_directory + media_image.hash
        image.save(output_path, format=image.format)
        return True

    def _create_video_thumbnail(self, media_video: Media) -> bool:
        #  TODO: Test.
        output_path = self.__thumbnail_directory + media_video.hash
        size = str(self.__height) + "x" + str(self.__width)
        FNULL = open(os.devnull, 'w')
        subprocess.call(['ffmpeg', '-i', media_video.path, '-ss', '00:00:01.000',
            '-vframes', '1', '-s', size, '-f', 'image2', output_path], stdout=FNULL, stderr=subprocess.STDOUT)
        return True
