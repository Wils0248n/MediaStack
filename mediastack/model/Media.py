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
    path = sa.Column('path', sa.String, nullable=True)
    category_name = sa.Column(sa.String, sa.ForeignKey('categories.name'), nullable=True)
    artist_name = sa.Column(sa.String, sa.ForeignKey('artists.name'), nullable=True)
    album_name = sa.Column(sa.String, sa.ForeignKey('albums.name'), nullable=True)

    type = sa.Column('type', sa.String)
    score = sa.Column('score', sa.Integer)
    source = sa.Column('source', sa.String)
    
    tags = sa.orm.relationship("Tag", secondary=MediaTag, back_populates="media")

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
