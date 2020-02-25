import sqlalchemy as sa
from model.Base import Base

media_tag_table = sa.Table('media_tag_relation', Base.metadata, 
    sa.Column('media', sa.String, sa.ForeignKey('media.hash')),
    sa.Column('tags', sa.String, sa.ForeignKey('tags.name')))
