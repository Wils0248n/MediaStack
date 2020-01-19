import sqlite3
from typing import List
from Media import Media


class TagTableManager:

    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.__conn = connection
        self.__cursor = cursor

    def create_table(self):
        self.__cursor.execute("""CREATE TABLE tags (
                        hash text
                    )""")

    def add_media(self, media: Media):
        self.__cursor.execute("INSERT INTO tags (hash) VALUES (?)", (media.hash,))
        self.add_tags(media.tags, media)

    def add_tags(self, tags: List[str], media: Media):
        for tag in tags:
            self.__create_tag(tag.lower())
            self.__add_media_to_tag(media, tag)

    def __create_tag(self, tag_name: str):
        try:
            self.__cursor.execute("ALTER TABLE tags ADD COLUMN \"" + tag_name + "\"")
        except sqlite3.OperationalError:
            pass

    def __add_media_to_tag(self, media: Media, tag_name: str):
        self.__cursor.execute("UPDATE tags SET \"" + tag_name + "\"=? WHERE hash = ?", (media.hash, media.hash,))

    def get_media_tags(self, media: Media) -> List[str]:
        tag_search_result = self.__cursor.execute("SELECT * FROM tags WHERE hash=?", (media.hash,)).fetchone()

        if tag_search_result is None:
            return []
        else:
            tag_search_result = tag_search_result[1:]

        all_tags = self.__get_column_names()[1:]

        tags = []
        for index in range(len(tag_search_result)):
            if not tag_search_result[index] is None:
                tags.append(all_tags[index])

        return tags

    def get_all_media_with_tag(self, tag: str):
        tag = tag.replace("'", "").replace('"', '')
        return self.__cursor.execute("SELECT \"" + tag + "\" FROM tags WHERE \"" + tag + "\" IS NOT NULL").fetchall()

    def __get_column_names(self) -> List[str]:
        results = self.__cursor.execute("PRAGMA table_info(tags)").fetchall()
        columns = []
        for result in results:
            columns.append(result[1])
        return columns
