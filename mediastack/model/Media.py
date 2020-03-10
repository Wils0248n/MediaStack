from enum import Enum
import sqlalchemy as sa
from mediastack.model.Base import Base
from mediastack.model.Album import Album
from mediastack.utility.MediaUtility import extract_media_meta, hash_file, extract_source, determine_media_type

MediaTag = sa.Table('media_tag', Base.metadata, 
    sa.Column('media', sa.String, sa.ForeignKey('media.hash')),
    sa.Column('tags', sa.String, sa.ForeignKey('tags.name')))

class Media(Base):
    __tablename__ = 'media'

    hash = sa.Column('hash', sa.String, primary_key=True)
    path = sa.Column('path', sa.String, nullable=True)
    category_name = sa.Column(sa.String, sa.ForeignKey('categories.name'), nullable=True)
    artist_name = sa.Column(sa.String, sa.ForeignKey('artists.name'), nullable=True)
    album_name = sa.Column(sa.String, sa.ForeignKey('albums.name'), nullable=True)

    type = sa.Column('type', sa.String)
    score = sa.Column('score', sa.Integer)
    source = sa.Column('source', sa.String)
    
    tags = sa.orm.relationship("Tag", secondary=MediaTag, back_populates="media")

    def _get_album(self) -> Album:
        return sa.orm.Session.object_session(self).query(Album).filter(Album.name == self.album_name).first()

    def _get_album_index(self) -> int:
        album = self._get_album()
        if album is None:
            return 0
        album_media = album.media
        album_media.sort()
        return album_media.index(self)

    album_index = property(_get_album_index)

    def _get_next_media(self):
        if self.album_name is None:
            return self
        else:
            album_media = self._get_album().media
            album_media.sort()
            current_index = album_media.index(self)
            if current_index == len(album_media) - 1:
                return album_media[0]
            else:
                return album_media[current_index + 1]

    next_media = property(_get_next_media)

    def _get_previous_media(self):
        if self.album_name is None:
            return self
        else:
            album_media = self._get_album().media
            album_media.sort()
            current_index = album_media.index(self)
            if current_index == 0:
                return album_media[len(album_media) - 1]
            else:
                return album_media[current_index - 1]

    previous_media = property(_get_previous_media)

    def __hash__(self):
        return hash(self.hash)

    def __lt__(self, other):
        if self.category == other.category:
            return self.path < other.path
        else:
            return self.category.name < other.category.name

    def __gt__(self, other):
        if self.category == other.category:
            return self.path > other.path
        else:
            return self.category.name > other.category.name

    def __eq__(self, other):
        return self.hash == other.hash