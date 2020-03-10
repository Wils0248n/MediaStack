import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.model.Media import MediaTag

class Tag(Base):
    __tablename__ = 'tags'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship("Media", secondary=MediaTag, back_populates="tags")

    media_count = sa.orm.column_property(
        sa.sql.expression.select(
            [sa.sql.expression.func.count(MediaTag.c.media)])
        .where(MediaTag.c.tags == name)
        .correlate_except(MediaTag))

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other):
        return self.name == other

    def __repr__(self):
        return self.name
