import hashlib, os
from PIL import Image
from io import StringIO

def hashFile(filePath):
    hasher = hashlib.md5()
    with open(filePath, 'rb') as file:
        buffer = file.read()
        hasher.update(buffer)
    return hasher.hexdigest()

def thumbnail_image(imagePath):
    image = Image.open(imagePath)
    image.thumbnail((225, 175))
    thumb_buffer = StringIO()
    outputPath = os.getcwd() + "/thumbs/" + hashFile(imagePath)
    image.save(outputPath, format=image.format)
