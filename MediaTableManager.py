from Media import Media


class MediaTableManager:

    def __init__(self, connection, cursor):
        self.conn = connection
        self.cursor = cursor

    def create_table(self):
        self.cursor.execute("""CREATE TABLE imagedata (
                        hash text,
                        filename text,
                        category text,
                        artist text,
                        album text,
                        source text
                    )""")

    def initialize_table(self, media_list):
        for media in media_list:
            self.add_media(media)

    def add_media(self, media):
        self.cursor.execute("INSERT INTO imagedata VALUES (?, ?, ?, ?, ?, ?)",
                            (media.hash, media.path, media.category, media.artist, media.album, media.source))

    def remove_media(self, media):
        self.cursor.execute("DELETE FROM imagedata WHERE hash=?", (media.hash,))

    def get_media(self, media_hash):
        return create_media(self.cursor.execute("SELECT * FROM imagedata WHERE hash=?", (media_hash,)).fetchone())

    def get_all_media(self):
        media_list = []
        for media_data in self.cursor.execute("SELECT * FROM imagedata").fetchall():
            try:
                media_list.append(create_media(media_data))
            except FileNotFoundError:
                pass  # TODO: Handle missing file.
        return media_list


def create_media(media_data):
    return Media(media_data[1], media_hash=media_data[0], category=media_data[2], artist=media_data[3], album=media_data[4], source=media_data[5])