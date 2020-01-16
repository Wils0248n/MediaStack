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

    def convertFromListOfTuplesToList(self, tupleList):
        result = []
        for tuple in tupleList:
            result.append(tuple[0])
        return result

    def addImageToDB(self, image):
        if not thumbnailImage(image):
            return

        imagePath = image.replace(self.rootDir + os.path.sep, '')
        imagePath = imagePath.split(os.path.sep)

        if len(imagePath) < 2:
            return

        hash = hashFile(image)
        album = imagePath[2] if len(imagePath) == 4 else "noalbum"

        self.cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?)",
        (hash, image, imagePath[0], imagePath[1], album, getImageSource(image)))

        self.cursor.execute("INSERT INTO tags (hash) VALUES (?)", (hash,))

        self.addTagsToDB(getImageTags(image), hash)

    def addTagsToDB(self, tags, hash):
        for tag in tags:
            self.createTagInDB(tag.lower())
            self.addImageHashToTagDB(tag, hash)

    def createTagInDB(self, tagName):
        try:
            self.cursor.execute("ALTER TABLE tags ADD COLUMN \"" + tagName + "\"")
        except sqlite3.OperationalError:
            pass

    def addImageHashToTagDB(self, tagName, imageHash):
        self.cursor.execute("UPDATE tags SET \"" + tagName + "\"=? WHERE hash = ?", (imageHash, imageHash,))

    def getImageTags(self, imageHash):
        tagSearchResult = self.cursor.execute("SELECT * FROM tags WHERE hash=?", (imageHash,)).fetchone()

        if tagSearchResult == None:
            return []
        else:
            tagSearchResult = tagSearchResult[1:]

        allTags = self.getColumnNames("tags")[1:]

        tags = []
        for index in range(len(tagSearchResult)):
            if not tagSearchResult[index] == None:
                tags.append(allTags[index])

        return tags

    def getAllImagesWithTag(self, tag):
        tag = tag.replace("'", "").replace('"', '')
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

    def removeImagesFromListThatContainsTag(self, imageList, tag):
        return [image for image in imageList if not self.doesImageContainTag(image, tag)]

    def removeImagesFromListThatContainTags(self, imageList, tags):
        for tag in tags:
            print(tag)
            imageList = self.removeImagesFromListThatContainsTag(imageList, tag)
        return imageList

    def doesImageContainTag(self, image, imageTag):
        return len([tag for tag in self.getImageTags(image) if tag == imageTag]) > 0

    def doesImageContainTags(self, image, tags):
        for tag in tags:
            if not self.doesImageContainTag(image, tag):
                return False
        return True

    def removeImagesThatDontContainTags(self, imageList, tags):
        return [image for image in imageList if self.doesImageContainTags(image, tags)]

    def getImagesThatContainTags(self, tags):
        imageList = []
        for tag in tags:
            imageList = list(set( imageList + self.getAllImagesWithTag(tag) ))

        return self.convertFromListOfTuplesToList(imageList)

    def searchDatabase(self, tags):
        whitelistTags = []
        blacklistTags = []

        for tag in tags:
            if tag[0] == "-":
                blacklistTags.append(tag[1:])
            else:
                whitelistTags.append(tag)

        imageList = self.getImagesThatContainTags(whitelistTags)
        imageList = self.removeImagesThatDontContainTags(imageList, whitelistTags)
        imageList = self.removeImagesFromListThatContainTags(imageList, blacklistTags)

        return self.getImageDataFromListOfHashes(imageList)

    def getImageDataFromListOfHashes(self, hashList):
        imageDataList = []

        for hash in hashList:
            imageDataList.append(self.getImageDataWithHash(hash))

        return imageDataList

if __name__ == '__main__':
    dbm = databaseManager("photos")
    print(dbm.searchDatabase([]))
    dbm.conn.close()