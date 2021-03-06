import sqlalchemy as sa
from typing import List
from mediastack.model.Base import Base

AlbumTag = sa.Table('album_tag', Base.metadata, 
    sa.Column('album', sa.Integer, sa.ForeignKey('albums.id')),
    sa.Column('tag', sa.Integer, sa.ForeignKey('tags.id')))

class Album(Base):
    __tablename__ = 'albums'

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String, unique=False)
    artist_id = sa.Column(sa.Integer, sa.ForeignKey('artists.id'), nullable=False)
    category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'), nullable=False)

    media = sa.orm.relationship('Media', backref='album', lazy='select')
    tags = sa.orm.relationship("Tag", secondary=AlbumTag, back_populates="albums")

    def _cover(self):
        if len(self.media) == 0:
            return None
        self.media.sort()
        return [media for media in self.media if media.path is not None][0]

    cover = property(_cover)

    def get_media_tags(self):
        tags = []
        for media in self.media:
            for tag in media.tags:
                if tag not in tags:
                    tags.append(tag)
        return tags

    def _score(self):
        if self.cover is not None:
            return self.cover.score

    score = property(_score)

    def _types(self):
        types = []
        for media in self.media:
            if media.type not in types:
                types.append(media.type)
        return types

    types = property(_types)

    def __init__(self, name: str) -> None:
        if name is None or len(name) == 0:
            raise ValueError("Invalid album name.")
        self.name = name

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name
