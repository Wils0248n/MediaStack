from flask_restful import Resource
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class TagsResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        return Response(ResponseType.OK, data=[{'id':tag.id, 'name':tag.name} for tag in self._media_manager.get_tags()]).getResponse()

class TagCreationResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager
    
    def post(self, tag_name):
        tag = self._media_manager.find_tag_by_name(tag_name)
        if tag is not None:
            return Response(ResponseType.BAD_REQUEST, message="Duplicate tag name.").getResponse()
        
        tag = self._media_manager.create_tag(tag_name)
        return Response(ResponseType.CREATED, data={'id':tag.id, 'name':tag.name}).getResponse()

class TagInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, tag_id):
        try:
            tag_id = int(tag_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid tag id.").getResponse()
        tag = self._media_manager.find_tag_by_id(tag_id)
        if tag is None:
            return Response(ResponseType.NOT_FOUND, message="Tag not found.").getResponse()
        
        return Response(ResponseType.OK, data={'tag':Serializer.serialize_tag(tag)}).getResponse()
