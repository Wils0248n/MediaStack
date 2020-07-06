from flask_restful import Resource
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class ArtistsResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        return Response(ResponseType.OK, data=[{'id':artist.id, 'name':artist.name} for artist in self._media_manager.get_artists()]).getResponse()
    
class ArtistInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, artist_id: str):
        try:
            artist_id = int(artist_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid artist id.").getResponse()
        artist = self._media_manager.find_artist_by_id(artist_id)
        if artist is None:
            return Response(ResponseType.NOT_FOUND, message="Artist not found.").getResponse()

        return Response(ResponseType.OK, data=Serializer.serialize_artist(artist)).getResponse()
    