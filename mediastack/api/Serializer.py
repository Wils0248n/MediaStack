from typing import Dict
from mediastack.model.Media import Media
from mediastack.model.Tag import Tag
from mediastack.model.Album import Album
from mediastack.model.Artist import Artist
from mediastack.model.Category import Category

class Serializer():
    
    @staticmethod
    def serialize_media(media: Media) -> Dict:
        if media is None:
            return None
        
        serialized_media = {}
        serialized_media['hash'] = media.hash
        serialized_media['category'] = media.category_name
        serialized_media['artist'] = media.artist_name
        serialized_media['album'] = media.album_name
        serialized_media['source'] = media.source
        serialized_media['score'] = media.score
        serialized_media['type'] = media.type
        serialized_media['tags'] = [tag.name for tag in media.tags]

        return serialized_media

    @staticmethod
    def serialize_album(album: Album) -> Dict:
        if album is None:
            return None
        serialized_album = {}

        serialized_album['name'] = album.name
        serialized_album['cover'] = album.cover.hash
        serialized_album['media'] = [media.hash for media in album.media]
        serialized_album['tags'] = [tag.name for tag in album.tags]

        return serialized_album

    @staticmethod
    def serialize_tag(tag: Tag) -> Dict:
        if tag is None:
            return None
        serialized_tag = {}
        serialized_tag['name'] = tag.name
        serialized_tag['media'] = [media.hash for media in tag.media]

        return serialized_tag
    
    @staticmethod
    def serialize_artist(artist: Artist) -> Dict:
        if artist is None:
            return None
        serialized_artist = {}
        serialized_artist['name'] = artist.name
        serialized_artist['media'] = [media.hash for media in artist.media]

        return serialized_artist

    @staticmethod
    def serialize_category(category: Category) -> Dict:
        if category is None:
            return None
        serialized_category = {}
        serialized_category['name'] = category.name
        serialized_category['media'] = [media.hash for media in category.media]

        return serialized_category
