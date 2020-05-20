from flask_restful import Resource
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class TagsResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        return Response(ResponseType.OK, data={'tags':[tag.name for tag in self._media_manager.get_tags()]}).getResponse()

class TagInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, tag_id):
        tag = self._media_manager.find_tag(tag_id)
        if tag is None:
            return Response(ResponseType.NOT_FOUND, message="Tag not found.").getResponse()
        
        return Response(ResponseType.OK, data={'tag':Serializer.serialize_tag(tag)}).getResponse()