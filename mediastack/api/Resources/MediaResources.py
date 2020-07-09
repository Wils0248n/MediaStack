import os, time
from flask_restful import Resource
from flask import send_file, send_from_directory, request
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class MediaResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        return Response(ResponseType.OK, data=[Serializer.serialize_media(media) for media in self._media_manager.get_media()]).getResponse()

class MediaFileResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, media_id):
        try:
            media_id = int(media_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid media id.").getResponse()
        media = self._media_manager.find_media_by_id(media_id)
        if media is not None:
            return send_from_directory(os.getcwd(), media.path, as_attachment=True)
            
        return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()

class MediaThumbnailFileResource(Resource):
    def __init__(self, media_manager: MediaManager):
            self._media_manager = media_manager
        
    def get(self, media_id):
        try:
            media_id = int(media_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid media id.").getResponse()
        media = self._media_manager.find_media_by_id(media_id)
        if media is None:
            return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()
        
        if os.path.isfile("thumbs/" + media.hash) is not None:
            return send_from_directory(os.getcwd(), "thumbs/" + media.hash, as_attachment=True)
        
        return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()

class MediaInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, media_id):
        try:
            media_id = int(media_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid media id.").getResponse()
        media = self._media_manager.find_media_by_id(media_id)
        if media is not None:
            response = Response(ResponseType.OK, data=Serializer.serialize(media))
        else:
            response = Response(ResponseType.NOT_FOUND, message="Media not found.")
        
        return response.getResponse()

    def put(self, media_id):
        try:
            media_id = int(media_id)
        except ValueError:
            return Response(ResponseType.BAD_REQUEST, message="Invalid media id.").getResponse()
        media = self._media_manager.find_media_by_id(media_id)
        try:
            if media is not None:
                new_media_info = request.get_json()
                if 'score' in new_media_info.keys():
                    self._media_manager.change_media_score(media, new_media_info['score'])
                if 'source' in new_media_info.keys():
                    self._media_manager.change_media_source(media, new_media_info['source'])
                if 'tags' in new_media_info:
                    new_tags = []
                    for tag_id in new_media_info['tags']:
                        tag = self._media_manager.find_tag_by_id(tag_id)
                        if tag is None:
                            return Response(ResponseType.BAD_REQUEST, message="Invalid tag id: {}".format(str(tag_id))).getResponse()

                        new_tags.append(tag)

                    self._media_manager.change_media_tags(media, new_tags)
                response = Response(ResponseType.OK, data=Serializer.serialize(media))
            else:
                response = Response(ResponseType.NOT_FOUND, message="Media not found.")
        except TypeError:
            response = Response(ResponseType.BAD_REQUEST, message="Bad media data.")

        return response.getResponse()
