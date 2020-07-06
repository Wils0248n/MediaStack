import json
from flask_restful import Resource
from flask import request
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType
from mediastack.controller.search.SearchManager import SearchManager
from mediastack.controller.search.SearchParser import SearchError

class SearchResource(Resource):
    def __init__(self, search_manager: SearchManager):
        self._search_manager = search_manager
    
    def get(self):
        try:
            search_result = self._search_manager.search(None)
            resulting_media = search_result[0]
            resulting_albums = search_result[1]
            data = {
                "media": [Serializer.serialize_media(media) for media in search_result[0]],
                "albums": [Serializer.serialize_album(album) for album in search_result[1]]
            }
            return Response(ResponseType.OK, data=data).getResponse()
        except SearchError as e:
            return Response(ResponseType.NOT_FOUND, message=str(e)).getResponse()

    def post(self):
        try:
            search_result = self._search_manager.search(request.get_json())
            resulting_media = search_result[0]
            resulting_albums = search_result[1]
            data = {
                "media": [Serializer.serialize_media(media) for media in search_result[0]],
                "albums": [Serializer.serialize_album(album) for album in search_result[1]]
            }
            return Response(ResponseType.CREATED, data=data).getResponse()
        except SearchError as e:
            return Response(ResponseType.NOT_FOUND, message=str(e)).getResponse()
        except TypeError as e:
            return Response(ResponseType.BAD_REQUEST, data=str(e), message="Invalid search request.").getResponse()
    