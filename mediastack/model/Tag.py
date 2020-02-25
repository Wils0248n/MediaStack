import sqlalchemy as sa
from model.Base import Base
from model.Media import Media
from model.Relations import media_tag_table

class Tag(Base):
    __tablename__ = 'tags'

    name = sa.Column('name', sa.String, primary_key=True)

    media = sa.orm.relationship("Media", 
    secondary=media_tag_table, 
    back_populates="tags")

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        return self.name