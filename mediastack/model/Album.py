import sqlalchemy as sa
from mediastack.model.Base import Base

class Album(Base):
    __tablename__ = 'albums'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship('Media', backref='album', lazy='select')

    def _get_cover(self):
        self.media.sort()
        return self.media[0]

    def _get_media_count(self):
        return len(self.media)

    cover = property(_get_cover)
    media_count = property(_get_media_count)

    def __init__(self, name: str) -> None:
        self.name = name