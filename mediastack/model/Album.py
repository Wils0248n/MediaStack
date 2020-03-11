import sqlalchemy as sa
from typing import List
from mediastack.model.Base import Base

AlbumTag = sa.Table('album_tag', Base.metadata, 
    sa.Column('album', sa.String, sa.ForeignKey('albums.name')),
    sa.Column('tag', sa.String, sa.ForeignKey('tags.name')))

class Album(Base):
    __tablename__ = 'albums'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship('Media', backref='album', lazy='select')

    def _get_cover(self):
        self.media.sort()
        return self.media[0]

    cover = property(_get_cover)

    def _get_media_count(self) -> int:
        return len(self.media)
    
    length = property(_get_media_count)

    tags = sa.orm.relationship("Tag", secondary=AlbumTag, back_populates="albums")

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other
