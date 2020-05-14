import sqlalchemy as sa
from mediastack.model.Base import Base

class Category(Base):
    __tablename__ = 'categories'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship('Media', backref='category', lazy='select')

    def __init__(self, name: str):
        if name is None or len(name) == 0:
            raise ValueError("Invalid artist name.")
        self.name = name

    def __eq__(self, other):
        return self.name == other
