from typing import Dict
from mediastack.model.Media import Media
from mediastack.model.Tag import Tag
from mediastack.model.Album import Album
from mediastack.model.Artist import Artist
from mediastack.model.Category import Category

class Serializer():
    
    @staticmethod
    def serialize(model_object) -> Dict:
        if isinstance(model_object, Media):
            return Serializer.serialize_media(model_object)
        if isinstance(model_object, Album):
            return Serializer.serialize_album(model_object)
        if isinstance(model_object, Tag):
            return Serializer.serialize_tag(model_object)
        if isinstance(model_object, Artist):
            return Serializer.serialize_artist(model_object)
        if isinstance(model_object, Category):
            return Serializer.serialize_category(model_object)
        raise RuntimeError("Could not serialize: " + type(model_object))

    @staticmethod
    def serialize_media(media: Media) -> Dict:
        if media is None:
            return None
        
        serialized_media = {}
        serialized_media['id'] = media.id
        serialized_media['hash'] = media.hash
        serialized_media['category_id'] = media.category_id
        serialized_media['artist_id'] = media.artist_id
        serialized_media['album_id'] = media.album_id
        serialized_media['source'] = media.source
        serialized_media['score'] = media.score
        serialized_media['type'] = media.type
        serialized_media['file'] = '/api/media/{}'.format(media.id)
        serialized_media['thumbnail'] = '/api/media/{}/thumbnail'.format(media.id)
        serialized_media['tags'] = [{'id':tag.id,'name':tag.name} for tag in media.tags]

        return serialized_media

    @staticmethod
    def serialize_album(album: Album) -> Dict:
        if album is None:
            return None
        serialized_album = {}

        serialized_album['id'] = album.id
        serialized_album['name'] = album.name
        serialized_album['cover_id'] = album.cover.id if album.cover is not None else None
        serialized_album['category_id'] = album.category_id
        serialized_album['artist_id'] = album.artist_id
        serialized_album['media'] = [Serializer.serialize(media) for media in album.media]
        serialized_album['tags'] = [{'id':tag.id,'name':tag.name} for tag in album.tags]

        return serialized_album

    @staticmethod
    def serialize_tag(tag: Tag) -> Dict:
        if tag is None:
            return None
        serialized_tag = {}
        serialized_tag['id'] = tag.id
        serialized_tag['name'] = tag.name
        serialized_tag['media'] = [media.id for media in tag.media]

        return serialized_tag
    
    @staticmethod
    def serialize_artist(artist: Artist) -> Dict:
        if artist is None:
            return None
        serialized_artist = {}
        serialized_artist['id'] = artist.id
        serialized_artist['name'] = artist.name
        serialized_artist['media'] = [media.id for media in artist.media]
        serialized_artist['albums'] = [album.id for album in artist.albums]

        return serialized_artist

    @staticmethod
    def serialize_category(category: Category) -> Dict:
        if category is None:
            return None
        serialized_category = {}
        serialized_category['id'] = category.id
        serialized_category['name'] = category.name
        serialized_category['media'] = [media.id for media in category.media]
        serialized_category['albums'] = [album.id for album in category.albums]

        return serialized_category
