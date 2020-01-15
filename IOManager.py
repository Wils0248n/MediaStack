import hashlib, os, json, logging
from PIL import Image, UnidentifiedImageError
from io import StringIO
from iptcinfo3 import IPTCInfo

iptcinfo_logger = logging.getLogger('iptcinfo')
iptcinfo_logger.setLevel(logging.ERROR)

thumbnailDirectory = "thumbs/"

def readFile(filePath):
    with open(os.getcwd() + filePath) as file:
        return file.read()

def readFileBytes(filePath):
    with open(os.getcwd() + filePath, 'rb') as file:
        return file.read()

def hashFile(filePath):
    if os.path.isdir(filePath):
        return
    hasher = hashlib.md5()
    with open(filePath, 'rb') as file:
        buffer = file.read()
        hasher.update(buffer)
    return hasher.hexdigest()

def thumbnailImage(imagePath):
    if os.path.isfile(thumbnailDirectory + hashFile(imagePath)):
        return True
    image = None
    try:
        image = Image.open(imagePath)
    except UnidentifiedImageError:
        return False
    image.thumbnail((225, 175))
    thumb_buffer = StringIO()
    outputPath = os.getcwd() + os.path.sep + thumbnailDirectory + hashFile(imagePath)
    image.save(outputPath, format=image.format)
    return True

def getImageTags(imagePath):
    info = IPTCInfo(imagePath)
    keywords = []
    for keyword in info['keywords']:
        keywords.append(keyword.decode("utf-8"))
    return json.dumps(keywords)

def scanImageDirectory(rootDir):
    images = []
    for currentDirectory, directories, files in os.walk(rootDir):
        for file in files:
            currentPath = os.path.join(currentDirectory, file)
            if thumbnailImage(currentPath):
                images.append(currentPath)
    return images

if __name__ == '__main__':
    print(scanImageDirectory("photos"))