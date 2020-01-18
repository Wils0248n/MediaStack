from Media import Media
from SearchManager import SearchManager
from DBManager import DatabaseManager
import os


class MediaManager:

    def __init__(self):
        self.media_list = []
        self.db_manager = DatabaseManager()
        self.initialize()

    def initialize(self):
        try:
            self.db_manager.create_database()
            print("Created tables...\nInitializing Media...")
            self.initialize_media_from_directory("photos/")
            print("Done.\nAdding Media to DB...")
            self.add_media_to_database()
            print("Done.")
        except RuntimeError:
            print("Database exists...\nInitializing from DB...")
            self.initialize_media_from_database()
            print("Done.")

    def add_media(self, media):
        if media in self.media_list:
            return
        self.media_list.append(media)

    def initialize_media_from_database(self):
        for media in self.db_manager.get_all_media():
            if media.create_thumbnail("thumbs/"):
                self.add_media(media)

    def initialize_media_from_directory(self, root_directory):
        for currentDirectory, directories, files in os.walk(root_directory):
            for file in files:
                try:
                    media = Media(os.path.join(currentDirectory, file))
                    if media.create_thumbnail("thumbs/"):
                        self.add_media(media)
                except ValueError:
                    pass  # TODO: Handle invalid file path.

    def add_media_to_database(self):
        for media in self.media_list:
            self.db_manager.add_media(media)
        self.db_manager.write_database_changes()

    def get_media(self, media_hash):
        for media in self.media_list:
            if media.hash == media_hash:
                return media

    def search(self, search_query):
        return SearchManager().search(self.media_list, search_query)


if __name__ == '__main__':
    i = MediaManager()
    i.initialize_media_from_directory("photos")
    for image in i.get_all_media():
        print(image)
