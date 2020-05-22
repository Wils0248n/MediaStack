import os
from flask_restful import Resource
from flask import send_file, send_from_directory
from mediastack.controller.MediaManager import MediaManager
from mediastack.api.Serializer import Serializer
from mediastack.api.Response import Response, ResponseType

class MediaResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self):
        data = {}
        for media in self._media_manager.get_media():
            data[media.hash] = Serializer.serialize_media(media)
        return Response(ResponseType.OK, data=data).getResponse()

class MediaFileResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, media_id):
        media = self._media_manager.find_media(media_id)
        if media is not None:
            return send_from_directory(os.getcwd(), media.path, as_attachment=True)
            
        return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()

class MediaThumbnailFileResource(Resource):
    def __init__(self, media_manager: MediaManager):
            self._media_manager = media_manager
        
    def get(self, media_id):
        if os.path.isfile("thumbs/" + media_id) is not None:
            return send_from_directory(os.getcwd(), "thumbs/" + media_id, as_attachment=True)
        
        return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()

class MediaInfoResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def get(self, media_id):
        media = self._media_manager.find_media(media_id)
        if media is not None:
            data = {}
            data['media'] = Serializer.serialize_media(media)
            next_media = self._media_manager.get_next_media_in_album(media)
            previous_media = self._media_manager.get_previous_media_in_album(media)
            data['next_media'] = None if next_media is None else next_media.hash
            data['previous_media'] = None if previous_media is None else previous_media.hash
            response = Response(ResponseType.OK, data=data)
        else:
            response = Response(ResponseType.NOT_FOUND, message="Media not found.")
        
        return response.getResponse()

class MediaMutateTagsResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager

    def delete(self, media_id: str, tag_id: str):
        media = self._media_manager.find_media(media_id)
        if media is None:
            return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()
        tag = self._media_manager.find_tag(tag_id)
        if tag is None:
            return Response(ResponseType.NOT_FOUND, message="Tag not found.").getResponse()
        
        if self._media_manager.remove_tag_from_media(media, tag) is not None:
            return Response(ResponseType.OK).getResponse()
        else:
            return Response(ResponseType.BAD_REQUEST, message="Media does not contain that tag.").getResponse()

    def post(self, media_id: str, tag_id: str):
        media = self._media_manager.find_media(media_id)
        if media is None:
            return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()
        
        tag = self._media_manager.find_tag(tag_id)
        if tag is None:
            tag = self._media_manager.create_tag(tag_id)
        if self._media_manager.add_tag_to_media(media, tag) is not None:
            return Response(ResponseType.CREATED).getResponse()
        else:
            return Response(ResponseType.BAD_REQUEST, message="Media already contains tag.").getResponse()

class MediaMutateSourceResouce(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager
    
    def put(self, media_id: str, source: str):
        media = self._media_manager.find_media(media_id)
        if media is None:
            response = Response(ResponseType.NOT_FOUND, message="Media not found.")
        else:
            self._media_manager.change_media_source(media, source)
            response = Response(ResponseType.OK)

        return response.getResponse()
        
class MediaMutateScoreResource(Resource):
    def __init__(self, media_manager: MediaManager):
        self._media_manager = media_manager
    
    def put(self, media_id: str, score: str):
        media = self._media_manager.find_media(media_id)
        if media is None:
            return Response(ResponseType.NOT_FOUND, message="Media not found.").getResponse()
        
        if self._media_manager.change_media_score(media, score) is None:
            return Response(ResponseType.BAD_REQUEST, message="Invalid score.").getResponse()
        
        return Response(ResponseType.OK).getResponse()
