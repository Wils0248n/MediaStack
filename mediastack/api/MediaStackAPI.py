from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from mediastack.api.Resources import *
from mediastack.controller.MediaManager import MediaManager
from mediastack.controller.search.SearchManager import SearchManager

class MediaStackAPI():
    def __init__(self, media_manager: MediaManager, search_manager: SearchManager):
        self._app = Flask(__name__)
        self._api = Api(self._app)
        self._cors = CORS(self._app, resources={r"/api/*": {"origins": "*"}})
        self._media_manager = media_manager
        self._search_manager = search_manager
        self._add_media_resouces()
        self._add_album_resources()
        self._add_tag_resources()
        self._add_artist_resources()
        self._add_category_resources()
        self._add_search_resources()

    def _add_media_resouces(self):
        self._api.add_resource(MediaResource, '/api/media',
            resource_class_kwargs={'media_manager': self._media_manager})

        self._api.add_resource(MediaFileResource, '/api/media/<string:media_id>',
            resource_class_kwargs={'media_manager': self._media_manager})

        self._api.add_resource(MediaThumbnailFileResource, '/api/media/<string:media_id>/thumbnail',
            resource_class_kwargs={'media_manager': self._media_manager})

        self._api.add_resource(MediaInfoResource, '/api/media/<string:media_id>/info',
            resource_class_kwargs={'media_manager': self._media_manager})

    def _add_album_resources(self):
        self._api.add_resource(AlbumsResource, '/api/albums',
            resource_class_kwargs={'media_manager': self._media_manager})
        
        self._api.add_resource(AlbumInfoResource, '/api/albums/<string:album_id>/info',
            resource_class_kwargs={'media_manager': self._media_manager})
    
    def _add_tag_resources(self):
        self._api.add_resource(TagsResource, '/api/tags',
            resource_class_kwargs={'media_manager': self._media_manager})

        self._api.add_resource(TagCreationResource, '/api/tags/<string:tag_name>',
            resource_class_kwargs={'media_manager': self._media_manager})

        self._api.add_resource(TagInfoResource, '/api/tags/<string:tag_id>/info',
            resource_class_kwargs={'media_manager': self._media_manager})

    def _add_artist_resources(self):
        self._api.add_resource(ArtistsResource, '/api/artists',
            resource_class_kwargs={'media_manager': self._media_manager})

        self._api.add_resource(ArtistInfoResource, '/api/artists/<string:artist_id>/info',
            resource_class_kwargs={'media_manager': self._media_manager})

    def _add_category_resources(self):
        self._api.add_resource(CategoriesResource, '/api/categories',
            resource_class_kwargs={'media_manager': self._media_manager})

        self._api.add_resource(CategoryInfoResource, '/api/categories/<string:category_id>/info',
            resource_class_kwargs={'media_manager': self._media_manager})

    def _add_search_resources(self):
        self._api.add_resource(SearchResource, '/api/search',
            resource_class_kwargs={'search_manager': self._search_manager})
        
    def run(self):
        self._app.run(host='0.0.0.0', port=8000)
    