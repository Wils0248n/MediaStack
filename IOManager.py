import hashlib, os
from PIL import Image, UnidentifiedImageError
from io import StringIO
from DatabaseManager import databaseManager

thumbnailDirectory = "thumbs/"

def readFile(filePath):
    with open(os.getcwd() + os.path.sep + filePath) as file:
        return file.read()

def readFileBytes(filePath):
    with open(os.getcwd() + os.path.sep + filePath, 'rb') as file:
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
        print("Can't thumbnail image: " + imagePath)
        return False
    image.thumbnail((225, 175))
    thumb_buffer = StringIO()
    outputPath = os.getcwd() + os.path.sep + thumbnailDirectory + hashFile(imagePath)
    image.save(outputPath, format=image.format)
    print("Thumbnailing: " + imagePath)
    return True

def getImageTags(imagePath):
    return "notags"

def initializeDataBase(databaseManager, rootDir):
    currentPath = rootDir
    for categoryDir in os.listdir(currentPath):
        currentPath = os.path.sep.join([rootDir, categoryDir])
        if os.path.isdir(currentPath):
            for artistDir in os.listdir(currentPath):
                currentPath = os.path.sep.join([rootDir, categoryDir, artistDir])
                if os.path.isdir(currentPath):
                    for artistFile in os.listdir(currentPath):
                        currentPath = os.path.sep.join([rootDir, categoryDir, artistDir, artistFile])
                        if os.path.isfile(currentPath) and thumbnailImage(currentPath):
                            databaseManager.addImageToDB(hashFile(currentPath), currentPath, categoryDir, artistDir, "noalbum", getImageTags(currentPath))
                        elif os.path.isdir(currentPath):
                            for image in os.listdir(currentPath):
                                currentPath = os.path.sep.join([rootDir, categoryDir, artistDir, artistFile, image])
                                if (thumbnailImage(currentPath)):
                                    databaseManager.addImageToDB(hashFile(currentPath), currentPath, categoryDir, artistDir, artistFile, getImageTags(currentPath))

if __name__ == '__main__':
    initializeDataBase(databaseManager(), "/home/wilson/Pictures")
