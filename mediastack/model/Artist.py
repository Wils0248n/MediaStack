import sqlalchemy as sa
from mediastack.model.Base import Base

class Artist(Base):
    __tablename__ = 'artists'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship('Media', backref='artist', lazy='select')

    def __init__(self, name: str):
        self.name = name