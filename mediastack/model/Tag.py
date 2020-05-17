import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.model.Media import MediaTag
from mediastack.model.Album import AlbumTag

class Tag(Base):
    __tablename__ = 'tags'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship("Media", secondary=MediaTag, back_populates="tags")
    albums = sa.orm.relationship("Album", secondary=AlbumTag, back_populates="tags")

    def __init__(self, name: str) -> None:
        if name is None or len(name) == 0:
            raise ValueError("Invalid tag name.")
        self.name = name

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name
    
