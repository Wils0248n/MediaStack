from flask_restful import Resource
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType
from mediastack.controller.search.SearchManager import SearchManager
from mediastack.controller.search.SearchParser import SearchError
from mediastack.controller.search.MediaSet import MediaSet

class MediaSetResource(Resource):
    def __init__(self, search_manager: SearchManager):
        self._search_manager = search_manager
    
    def get(self):
        data = {}
        data['media_sets'] = {
            'media': {
                'identifier':'media',
                'description':'The set of media that is not within an album.'
            },
            'albums': {
                'identifier':'albums',
                'description':'The set of all cover media for all albums.'
            },
            'general': {
                'identifier':'general',
                'description':'The set of all covers to all albums and all media that is not within an album.'
            },
            'all': {
                'identifier':'all',
                'description':'The set of all media.'
            }
        }
        return Response(ResponseType.OK, data=data).getResponse()


class SearchMediaSetResource(Resource):
    def __init__(self, search_manager: SearchManager):
        self._search_manager = search_manager
    
    def get(self, media_set: str):
        search_media = self._search_manager.search(media_set, None)
        search_media.sort()
        return Response(ResponseType.OK, data=[Serializer.serialize_media(media) for media in search_media]).getResponse()

class SearchResouce(Resource):
    def __init__(self, search_manager: SearchManager):
        self._search_manager = search_manager

    def get(self, media_set: str, query_string: str):
        try:
            search_media = self._search_manager.search(media_set, query_string)
            search_media.sort()
            return Response(ResponseType.OK, data=[Serializer.serialize_media(media) for media in search_media]).getResponse()
        except SearchError as e:
            return Response(ResponseType.BAD_REQUEST, message=str(e)).getResponse()
