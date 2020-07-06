import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.model.Album import Album

MediaTag = sa.Table('media_tag', Base.metadata, 
    sa.Column('media', sa.Integer, sa.ForeignKey('media.id')),
    sa.Column('tags', sa.Integer, sa.ForeignKey('tags.id')))

class Media(Base):
    __tablename__ = 'media'

    id = sa.Column('id', sa.Integer, primary_key=True)
    hash = sa.Column('hash', sa.String, unique=True)
    path = sa.Column('path', sa.String, nullable=True)
    category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.id'), nullable=True)
    artist_id = sa.Column(sa.Integer, sa.ForeignKey('artists.id'), nullable=True)
    album_id = sa.Column(sa.Integer, sa.ForeignKey('albums.id'), nullable=True)

    type = sa.Column('type', sa.String, nullable=False)
    score = sa.Column('score', sa.Integer, nullable=True)
    source = sa.Column('source', sa.String, nullable=True)
    
    tags = sa.orm.relationship("Tag", secondary=MediaTag, back_populates="media")

    def __hash__(self):
        return hash(self.hash)

    def __lt__(self, other):
        if other is None:
            return False
        return self.path < other.path

    def __gt__(self, other):
        if other is None:
            return True
        return self.path > other.path

    def __eq__(self, other):
        if other is None:
            return False
        return self.hash == other.hash
