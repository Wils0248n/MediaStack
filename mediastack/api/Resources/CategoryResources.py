from flask_restful import Resource
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class CategoriesResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        data = {}
        for category in self._media_manager.get_categories():
            data[category.name] = Serializer.serialize_category(category)
        return Response(ResponseType.OK, data=data).getResponse()
    
class CategoryInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, category_id: str):
        category = self._media_manager.find_category(category_id)
        if category is None:
            return Response(ResponseType.NOT_FOUND, message="Category not found.").getResponse()

        return Response(ResponseType.OK, data={'artist':Serializer.serialize_category(category)}).getResponse()