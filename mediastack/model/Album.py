import sqlalchemy as sa
from model.Base import Base
from model.Relations import media_tag_table

class Album(Base):
    __tablename__ = 'albums'

    name = sa.Column('name', sa.String, primary_key=True)
    cover = sa.Column('cover', sa.String, nullable=False)
    
