import sqlalchemy as sa
from typing import List
from mediastack.model.Base import Base

class Album(Base):
    __tablename__ = 'albums'

    name = sa.Column('name', sa.String, primary_key=True)
    media = sa.orm.relationship('Media', backref='album', lazy='select')

    def _get_cover(self):
        self.media.sort()
        return self.media[0]

    cover = property(_get_cover)

    def _get_media_count(self) -> int:
        return len(self.media)
    
    length = property(_get_media_count)

    def _get_media_tags(self):
        media_tags = []
        for media in self.media:
            for tag in media.tags:
                if tag not in media_tags:
                    media_tags.append(tag)
        return media_tags

    media_tags = property(_get_media_tags)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other