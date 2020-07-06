from flask_restful import Resource
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class CategoriesResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        return Response(ResponseType.OK, data=[{'id':category.id, 'name':category.name} for category in self._media_manager.get_categories()]).getResponse()
    
class CategoryInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, category_id: str):
        try:
            category_id = int(category_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid category id.").getResponse()
        category = self._media_manager.find_category_by_id(category_id)
        if category is None:
            return Response(ResponseType.NOT_FOUND, message="Category not found.").getResponse()

        return Response(ResponseType.OK, data=Serializer.serialize(category)).getResponse()