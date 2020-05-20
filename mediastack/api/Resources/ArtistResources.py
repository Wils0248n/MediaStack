from flask_restful import Resource
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class ArtistsResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        data = {}
        for artist in self._media_manager.get_artists():
            data[artist.name] = Serializer.serialize_artist(artist)
        return Response(ResponseType.OK, data=data).getResponse()
    
class ArtistInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, artist_id: str):
        artist = self._media_manager.find_artist(artist_id)
        if artist is None:
            return Response(ResponseType.NOT_FOUND, message="Artist not found.").getResponse()

        return Response(ResponseType.OK, data={'artist':Serializer.serialize_artist(artist)}).getResponse()