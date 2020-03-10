import sqlalchemy as sa
from mediastack.model.Base import Base

class Album(Base):
    __tablename__ = 'albums'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship('Media', backref='album', lazy='select')
    cover = sa.Column('cover', sa.String, nullable=False)

    def __init__(self, name: str, cover: str) -> None:
        self.name = name
        self.cover = cover