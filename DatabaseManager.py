import sqlite3, os
from sqlite3 import OperationalError
from IOManager import scanImageDirectory, hashFile, getImageTags, getImageSource, thumbnailImage

class databaseManager:
    def __init__(self, rootDir):
        self.rootDir = rootDir
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        self.createDataBase()
        self.verifyDatabase()

    def createDataBase(self):
        try:
            self.cursor.execute("""CREATE TABLE imagedata (
                hash text,
                filename text,
                category text,
                artist text,
                album text,
                tags text,
                source text
            )""")
            print("Initializing Database...")
            self.initializeDatabase()
            print("Done.")
            self.conn.commit()
        except OperationalError:
            pass

    def initializeDatabase(self):
        for image in scanImageDirectory(self.rootDir):
            self.addImageToDB(image)
        self.conn.commit()

    def addImageToDB(self, image):
        if not thumbnailImage(image):
            return
        imagePath = image.replace(self.rootDir + os.path.sep, '')
        imagePath = imagePath.split(os.path.sep)
        if len(imagePath) == 3:
            self.cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?, ?)", (hashFile(image), image, imagePath[0], imagePath[1], "noalbum", getImageTags(image), getImageSource(image)))
        elif len(imagePath) == 4:
            self.cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?, ?)", (hashFile(image), image, imagePath[0], imagePath[1], imagePath[2], getImageTags(image), getImageSource(image)))

    def removeImageFromDB(self, image):
        self.cursor.execute("DELETE FROM imagedata WHERE filename=?", (image,))

    def getAllImageData(self):
        self.cursor.execute("SELECT * FROM imagedata")
        return self.cursor.fetchall()

    def verifyDatabase(self):
        print("Verifing Database...")
        differingImageLists = self.identifyImageDifferences()

        newImages = differingImageLists[0]
        missingImages = differingImageLists[1]

        for image in missingImages:
            self.removeImageFromDB(image)

        for image in newImages:
            thumbnailImage(image)
            self.addImageToDB(image)

        self.conn.commit()
        print("Done.")

    def identifyImageDifferences(self):
        currentImageList = scanImageDirectory(self.rootDir)
        currentDatabaseImageList = self.cursor.execute("SELECT filename FROM imagedata").fetchall()

        imagesNotInDatabase = []
        missingImagesInDatabase = []

        for image in currentDatabaseImageList:
            if image[0] not in currentImageList:
                missingImagesInDatabase.append(image[0])

        for image in currentImageList:
            if (image,) not in currentDatabaseImageList:
                imagesNotInDatabase.append(image)

        return (imagesNotInDatabase, missingImagesInDatabase)

