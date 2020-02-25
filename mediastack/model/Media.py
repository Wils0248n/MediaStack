import sqlalchemy as sa
from model.Base import Base
from model.Relations import media_tag_table
from enum import Enum

class Media(Base):
    __tablename__ = 'media'

    hash = sa.Column('hash', sa.String, primary_key=True)
    path = sa.Column('path', sa.String, nullable=False)
    category = sa.Column('category', sa.String)
    artist = sa.Column('artist', sa.String)
    album = sa.Column('album', sa.String)
    type = sa.Column('type', sa.String)
    score = sa.Column('score', sa.Integer)
    source = sa.Column('source', sa.String)

    tags = sa.orm.relationship("Tag", 
    secondary=media_tag_table, 
    back_populates="media")

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