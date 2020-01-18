import sqlite3


class TagTableManager:

    def __init__(self, connection, cursor):
        self.conn = connection
        self.cursor = cursor

    def create_table(self):
        self.cursor.execute("""CREATE TABLE tags (
                        hash text
                    )""")

    def add_media(self, image):
        self.cursor.execute("INSERT INTO tags (hash) VALUES (?)", (image.hash,))
        self.add_tags(image.tags, image)

    def add_tags(self, tags, media):
        for tag in tags:
            self.create_tag(tag.lower())
            self.add_media_to_tag(media, tag)

    def create_tag(self, tag_name):
        try:
            self.cursor.execute("ALTER TABLE tags ADD COLUMN \"" + tag_name + "\"")
        except sqlite3.OperationalError:
            # Handles duplicate Tag
            pass

    def add_media_to_tag(self, media, tag_name):
        self.cursor.execute("UPDATE tags SET \"" + tag_name + "\"=? WHERE hash = ?", (media.hash, media.hash,))

    def get_media_tags(self, image):
        tag_search_result = self.cursor.execute("SELECT * FROM tags WHERE hash=?", (image.hash,)).fetchone()

        if tag_search_result is None:
            return []
        else:
            tag_search_result = tag_search_result[1:]

        all_tags = self.get_column_names()[1:]

        tags = []
        for index in range(len(tag_search_result)):
            if not tag_search_result[index] is None:
                tags.append(all_tags[index])

        return tags

    def get_all_media_with_tag(self, tag):
        tag = tag.replace("'", "").replace('"', '')
        return self.cursor.execute("SELECT \"" + tag + "\" FROM tags WHERE \"" + tag + "\" IS NOT NULL").fetchall()

    def get_column_names(self):
        results = self.cursor.execute("PRAGMA table_info(tags)").fetchall()
        columns = []
        for result in results:
            columns.append(result[1])
        return columns
