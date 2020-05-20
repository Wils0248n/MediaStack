from flask_restful import Resource
from mediastack.controller.SearchManager import SearchManager
from mediastack.api.Serializer import Serializer

class MediaSetResource(Resource):
    def __init__(self, search_manager: SearchManager):
        self._search_manager = search_manager
    
    def get(self, media_set: str):
        search_media = self._search_manager.search(media_set, [])
        search_media.sort()
        response = {'message':'', 'data':[media.hash for media in search_media]}
        return response, 200

class SearchResouce(Resource):
    def __init__(self, search_manager: SearchManager):
        self._search_manager = search_manager

    def get(self, media_set: str, query_string: str):
        search_media = self._search_manager.search(media_set, query_string.split(" "))
        search_media.sort()
        response = {'message':'', 'data':[Serializer.serialize_media(media) for media in search_media]}
        return response, 200