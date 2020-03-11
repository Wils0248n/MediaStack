import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.model.Media import MediaTag
from mediastack.model.Album import AlbumTag

class Tag(Base):
    __tablename__ = 'tags'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship("Media", secondary=MediaTag, back_populates="tags")
    albums = sa.orm.relationship("Album", secondary=AlbumTag, back_populates="tags")

    def _media_count(self):
        return len([media for media in self.media if media.album is None]) + len(self.albums)

    media_count = property(_media_count)

    def _all_media_count(self):
        return len(media)

    all_media_count = property(_all_media_count)

    def _album_count(self):
        return len(albums)

    album_count = property(_album_count)

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        return self.name
