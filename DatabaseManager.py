import sqlite3, os, json
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
                source text
            )""")

            self.cursor.execute("""CREATE TABLE tags (
                hash text
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

    def getColumnNames(self, table):
        results = self.cursor.execute("PRAGMA table_info(" + table + ")").fetchall()
        columns = []
        for result in results:
            columns.append(result[1])
        return columns

    def addImageToDB(self, image):
        if not thumbnailImage(image):
            return

        imagePath = image.replace(self.rootDir + os.path.sep, '')
        imagePath = imagePath.split(os.path.sep)

        hash = hashFile(image)
        album = imagePath[2] if len(imagePath) == 4 else "noalbum"

        self.cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?)",
        (hash, image, imagePath[0], imagePath[1], album, getImageSource(image)))

        self.cursor.execute("INSERT INTO tags (hash) VALUES (?)", (hash,))

        self.addTagsToDB(getImageTags(image), hash)

    def addTagsToDB(self, tags, hash):
        for tag in tags:
            self.createTagInDB(tag)
            self.addImageHashToTagDB(tag, hash)

    def createTagInDB(self, tagName):
        try:
            self.cursor.execute("ALTER TABLE tags ADD COLUMN \"" + tagName + "\"")
        except sqlite3.OperationalError:
            pass

    def addImageHashToTagDB(self, tagName, imageHash):
        self.cursor.execute("UPDATE tags SET \"" + tagName + "\"=? WHERE hash = ?", (imageHash, imageHash,))

    def getImageTags(self, imageHash):
        tagSearchResult = self.cursor.execute("SELECT * FROM tags WHERE hash=?", (imageHash,)).fetchone()[1:]
        allTags = self.getColumnNames("tags")[1:]

        tags = []
        for index in range(len(tagSearchResult)):
            if not tagSearchResult[index] == None:
                tags.append(allTags[index])

        return tags

    def getAllImagesWithTag(self, tag):
        return self.cursor.execute("SELECT \"" + tag + "\" FROM tags WHERE \"" + tag + "\" IS NOT NULL").fetchall()

    def removeImageFromDB(self, image):
        self.cursor.execute("DELETE FROM imagedata WHERE filename=?", (image,))

    def getAllImageData(self):
        return self.cursor.execute("SELECT * FROM imagedata").fetchall()

    def getImageDataWithHash(self, hash):
        return self.cursor.execute("SELECT * FROM imagedata WHERE hash=?", (hash,)).fetchone()

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

if __name__ == '__main__':
    dbm = databaseManager("photos")
    print(dbm.getImageTags("1e0da43f3ab047b7b4da16fdfd24d123"))
    dbm.conn.close()