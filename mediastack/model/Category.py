import sqlalchemy as sa
from mediastack.model.Base import Base

class Category(Base):
    __tablename__ = 'categories'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship('Media', backref='category', lazy='select')

    def __init__(self, name: str):
        self.name = name