from enum import Enum
import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.utility.MediaUtility import extract_media_meta, hash_file, extract_source, determine_media_type

MediaTag = sa.Table('media_tag', Base.metadata, 
    sa.Column('media', sa.String, sa.ForeignKey('media.hash')),
    sa.Column('tags', sa.String, sa.ForeignKey('tags.name')))

class Media(Base):
    __tablename__ = 'media'

    hash = sa.Column('hash', sa.String, primary_key=True)
    path = sa.Column('path', sa.String, nullable=False)
    category = sa.Column('category', sa.String)
    artist = sa.Column('artist', sa.String)
    album_name = sa.Column('album_name', sa.String, sa.ForeignKey('albums.name'))
    album_index = sa.Column('album_index', sa.Integer)
    type = sa.Column('type', sa.String)
    score = sa.Column('score', sa.Integer)
    source = sa.Column('source', sa.String)
    tags = sa.orm.relationship("Tag", secondary=MediaTag, back_populates="media")

    def __init__(self, media_path: str) -> None:
        meta = extract_media_meta(media_path)
        self.hash = hash_file(media_path)
        self.path = media_path
        self.category = meta["category"]
        self.artist = meta["artist"]
        self.album_name = meta["album"]
        self.source = extract_source(media_path)
        self.type = determine_media_type(media_path)
        self.score = 0

    def __lt__(self, other):
        if self.category == other.category:
            return self.path < other.path
        else:
            return self.category.name < other.category.name

    def __gt__(self, other):
        if self.category == other.category:
            return self.path > other.path
        else:
            return self.category.name > other.category.name
