from flask_restful import Resource
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class AlbumsResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        data = {}
        for album in self._media_manager.get_albums():
            data[album.name] = Serializer.serialize_album(album)
        return Response(ResponseType.OK, data=data).getResponse()

class AlbumInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, album_id: str):
        album = self._media_manager.find_album(album_id)
        if album is None:
            response = Response(ResponseType.NOT_FOUND, message="Album not found.")
        else:
            data = {}
            data['album'] = Serializer.serialize_album(album)
            data['album']['media'] = [Serializer.serialize_media(media) for media in album.media]
            response = Response(ResponseType.OK, data=data)

        return response.getResponse()

class AlbumMutateTagsResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def delete(self, album_id: str, tag_id: str):
        album = self._media_manager.find_album(album_id)
        if album is None:
            return Response(ResponseType.NOT_FOUND, message="Album not found.").getResponse()
        tag = self._media_manager.find_tag(tag_id)
        if tag is None:
            return Response(ResponseType.NOT_FOUND, message="Tag not found.").getResponse()
        
        if tag not in album.tags:
            return Response(ResponseType.BAD_REQUEST, message="Album does not contain that tag.").getResponse()

        for media in album.media:
            self._media_manager.remove_tag_from_media(media, tag)

        return Response(ResponseType.OK).getResponse()

    def post(self, album_id: str, tag_id: str):
        album = self._media_manager.find_album(album_id)
        if album is None:
            return Response(ResponseType.NOT_FOUND, message="Album not found.").getResponse()
        
        tag = self._media_manager.find_tag(tag_id)
        if tag is None:
            tag = self._media_manager.create_tag(tag_id)
        
        for media in album.media:
            self._media_manager.add_tag_to_media(media, tag)
        
        return Response(ResponseType.CREATED).getResponse()
    
class AlbumMutateSourceResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager
    
    def put(self, album_id: str, source: str):
        album = self._media_manager.find_media(album_id)
        if album is None:
            return Response(ResponseType.NOT_FOUND, message="Album not found.").getResponse()
        
        for media in album.media:
            self._media_manager.change_media_source(media, source)
        
        return Response(ResponseType.OK).getResponse()
    
class AlbumMutateScoreResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def put(self, album_id: str, score: str):
        album = self._media_manager.find_media(album_id)
        if album is None:
            return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()
        
        for media in album.media:
            if self._media_manager.change_media_score(album, score) is None:
                return Response(ResponseType.BAD_REQUEST, message="Invalid score.").getResponse()
        
        return Response(ResponseType.OK).getResponse()
