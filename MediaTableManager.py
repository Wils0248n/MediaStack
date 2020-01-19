import sqlite3
from typing import List, Tuple
from Media import Media


class MediaTableManager:

    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor):
        self.__conn = connection
        self.__cursor = cursor

    def create_table(self):
        self.__cursor.execute("""CREATE TABLE imagedata (
                        hash text,
                        filename text,
                        type text,
                        category text,
                        artist text,
                        album text,
                        source text
                    )""")

    def __initialize_table(self, media_list: List[Media]):
        for media in media_list:
            self.add_media(media)

    def add_media(self, media: Media):
        self.__cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?, ?)",
                              (media.hash, media.path, media.type.value, media.category, media.artist, media.album, media.source))

    def remove_media(self, media: Media):
        self.__cursor.execute("DELETE FROM imagedata WHERE hash=?", (media.hash,))

    def find_media(self, media_hash: str) -> Media:
        return create_media(self.__cursor.execute("SELECT * FROM imagedata WHERE hash=?", (media_hash,)).fetchone())

    def get_all_media(self) -> List[Media]:
        media_list = []
        for media_data in self.__cursor.execute("SELECT * FROM imagedata").fetchall():
            try:
                media_list.append(create_media(media_data))
            except FileNotFoundError:
                pass  # TODO: Handle missing file.
        return media_list


def create_media(media_data: Tuple[str, str, str, str, str, str, str]) -> Media:
    return Media(media_data[1], media_hash=media_data[0], media_type=media_data[2],
                 category=media_data[3], artist=media_data[4], album=media_data[5], source=media_data[6])
