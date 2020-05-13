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
    tags = sa.orm.relationship("Tag", secondary=AlbumTag, back_populates="albums")

    def get_cover(self):
        if len(self.media) == 0:
            return None
        self.media.sort()
        return self.media[0]

    def get_media_count(self) -> int:
        return len(self.media)

    def media_tags(self):
        tags = []
        for media in self.media:
            for tag in media.tags:
                if tag not in tags:
                    tags.append(tag)
        return tags

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other
