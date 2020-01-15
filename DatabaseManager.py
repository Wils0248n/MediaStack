import sqlite3, os
from sqlite3 import OperationalError
from IOManager import scanImageDirectory
from IOManager import hashFile, getImageTags

class databaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        self.createDataBase()

    def createDataBase(self):
        try:
            self.cursor.execute("""CREATE TABLE imagedata (
                hash text,
                filename text,
                category text,
                artist text,
                album text,
                tags text
            )""")
            self.conn.commit()
        except OperationalError:
            pass

    def addImageToDB(self, hash, filename, category, artist, album, tags):
        self.cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?)", (hash, filename, category, artist, album, tags))

    def initializeDatabase(self, rootDir):
        for image in scanImageDirectory(rootDir):
            imagePath = image.replace(rootDir + os.path.sep, '')
            imagePath = imagePath.split(os.path.sep)
            if len(imagePath) == 3:
                self.addImageToDB(hashFile(image), image, imagePath[0], imagePath[1], "noalbum", getImageTags(image))
            elif len(imagePath) == 4:
                self.addImageToDB(hashFile(image), image, imagePath[0], imagePath[1], imagePath[2], getImageTags(image))
        self.conn.commit()

if __name__ == '__main__':
    databaseManager().initializeDatabase("photos")
