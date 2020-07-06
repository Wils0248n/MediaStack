import sqlalchemy as sa
from mediastack.model.Base import Base

class Category(Base):
    __tablename__ = 'categories'

    id = sa.Column('id', sa.Integer, primary_key=True)
    name = sa.Column('name', sa.String, unique=True)
    albums = sa.orm.relationship('Album', backref='category', lazy='select')
    media = sa.orm.relationship('Media', backref='category', lazy='select')

    def __init__(self, name: str):
        if name is None or len(name) == 0:
            raise ValueError("Invalid category name.")
        self.name = name

    def __eq__(self, other):
        return self.name == other
