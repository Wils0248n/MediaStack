from PIL import Image
from Media import Media
import os
import subprocess

class Thumbnailer:

    def __init__(self, thumbnail_directory, height=175, width=225):
        self.thumbnail_directory = thumbnail_directory
        self.height = height
        self.width = width

    def create_thumbnail(self, media):
        if os.path.isfile(self.thumbnail_directory + media.hash):
            return

        if media.type == Media.Type.IMAGE:
            self.create_image_thumbnail(media)
        elif media.type == Media.Type.ANIMATED_IMAGE:
            self.create_image_thumbnail(media)
        elif media.type == Media.Type.VIDEO:
            self.create_video_thumbnail(media)

    def create_image_thumbnail(self, media_image):
        image = Image.open(media_image.path)
        image.thumbnail((self.width, self.height))
        output_path = self.thumbnail_directory + media_image.hash
        image.save(output_path, format=image.format)

    def create_video_thumbnail(self, media_video):
        output_path = self.thumbnail_directory + media_video.hash
        size = str(self.height) + "x" + str(self.width)
        FNULL = open(os.devnull, 'w')
        subprocess.call(['ffmpeg', '-i', media_video.path, '-ss', '00:00:01.000',
            '-vframes', '1', '-s', size, '-f', 'image2', output_path], stdout=FNULL, stderr=subprocess.STDOUT)