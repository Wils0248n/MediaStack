from flask import request
from flask_restful import Resource
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class AlbumsResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        return Response(ResponseType.OK, data=[{'id':album.id, 'name':album.name} for album in self._media_manager.get_albums()]).getResponse()

class AlbumInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, album_id: str):
        try:
            album_id = int(album_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid Album ID.").getResponse()

        album = self._media_manager.find_album_by_id(album_id)
        if album is None:
            response = Response(ResponseType.NOT_FOUND, message="Album not found.")
        else:
            response = Response(ResponseType.OK, data=Serializer.serialize(album))

        return response.getResponse()

    def put(self, album_id: int):
        try:
            album_id = int(album_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid Album ID.").getResponse()
        
        album = self._media_manager.find_album_by_id(album_id)
        if album is None:
            return Response(ResponseType.NOT_FOUND, message="Album not found.").getResponse()

        request_json = request.get_json()

        if 'category' in request_json.keys():
            category = self._media_manager.find_category_by_id(request_json['category'])
            if category is None:
                return Response(ResponseType.NOT_FOUND, message="Category not found: {}".format(request_json['category'])).getResponse()
            self._media_manager.change_album_category(album, category)

        if 'source' in request_json.keys():
            for media in album.media:
                self._media_manager.change_media_source(media, request_json['source'])

        if 'score' in request_json.keys():
            for media in album.media:
                self._media_manager.change_media_score(media, request_json['score'])

        if 'add_tags' in request_json.keys():
            tags = []
            for tag_id in request_json['add_tags']:
                tag = self._media_manager.find_tag_by_id(tag_id)
                if tag is None:
                    return Response(ResponseType.NOT_FOUND, message="Invalid tag_id in tags: {}".format(str(tag_id))).getResponse()
                tags.append(tag)

            for media in album.media:
                self._media_manager.change_media_tags(media, [tag for tag in tags if tag not in media.tags] + media.tags)

        if 'remove_tags' in request_json.keys():
            tags = []
            for tag_id in request_json['remove_tags']:
                tag = self._media_manager.find_tag_by_id(tag_id)
                if tag is None:
                    return Response(ResponseType.NOT_FOUND, message="Invalid tag_id in tags: {}".format(str(tag_id))).getResponse()
                tags.append(tag)

            for media in album.media:
                self._media_manager.change_media_tags(media, [tag for tag in media.tags if tag not in tags])

        return Response(ResponseType.OK, data=Serializer.serialize_album(album)).getResponse()
