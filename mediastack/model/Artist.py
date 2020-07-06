import sqlalchemy as sa
from mediastack.model.Base import Base

class Artist(Base):
    __tablename__ = 'artists'

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String, unique=True)
    media = sa.orm.relationship('Media', backref='artist', lazy='select')
    albums = sa.orm.relationship('Album', backref='artist', lazy='select')

    def __init__(self, name: str):
        if name is None or len(name) == 0:
            raise ValueError("Invalid artist name.")
        self.name = name

    def __eq__(self, other):
        return self.name == other
