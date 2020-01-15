import sqlite3, os
from sqlite3 import OperationalError
from IOManager import scanImageDirectory, hashFile, getImageTags, getImageSource

class databaseManager:
    def __init__(self, rootDir):
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        self.createDataBase(rootDir)

    def createDataBase(self, rootDir):
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
            self.initializeDatabase(rootDir)
            print("Done.")
            self.conn.commit()
        except OperationalError:
            pass

    def initializeDatabase(self, rootDir):
        for image in scanImageDirectory(rootDir):
            imagePath = image.replace(rootDir + os.path.sep, '')
            imagePath = imagePath.split(os.path.sep)
            if len(imagePath) == 3:
                self.addImageToDB(hashFile(image), image, imagePath[0], imagePath[1], "noalbum", getImageTags(image), getImageSource(image))
            elif len(imagePath) == 4:
                self.addImageToDB(hashFile(image), image, imagePath[0], imagePath[1], imagePath[2], getImageTags(image), getImageSource(image))
        self.conn.commit()

    def addImageToDB(self, hash, filename, category, artist, album, tags, source):
        self.cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?, ?)", (hash, filename, category, artist, album, tags, source))

    def getAllImageData(self):
        self.cursor.execute("SELECT * FROM imagedata")
        return self.cursor.fetchall()

if __name__ == '__main__':
    databaseManager("photos").initializeDatabase("photos")