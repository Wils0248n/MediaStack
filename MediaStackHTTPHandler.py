import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import unquote
from WebGenerator import WebGenerator
from MediaManager import MediaManager


media_directory = "media/"
thumbnail_directory = "thumbs/"
media_manager = MediaManager(media_directory, thumbnail_directory)
web_generator = WebGenerator(thumbnail_directory)


class MediaStackHTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        if self.path == "/style.css":
            self.__send_200_response('text/css')
            self.wfile.write(read_file_bytes("/style.css"))

        elif str.startswith(self.path, "/media="):
            self.__send_200_response('text/html')
            media_hash = self.path.split('=')[1]
            html_code = web_generator.generate_media_page(media_manager.find_media(media_hash))
            self.wfile.write(bytes(html_code, 'UTF-8'))

        elif str.startswith(self.path, "/album="):
            self.__send_200_response('text/html')
            album_query = self.path.split('=')[1].split('/')
            album_name = unquote(album_query[0])
            if len(album_query) == 2:
                current_index = self.path.split('/')[2]
                html_code = web_generator.generate_album_media_page(media_manager.get_albums()[album_name],
                                                                    int(current_index))
            elif len(album_query) == 1:
                html_code = web_generator.generate_album_page(media_manager.get_albums()[album_name])

            self.wfile.write(bytes(html_code, 'UTF-8'))

        elif str.startswith(self.path, "/" + media_directory) or str.startswith(self.path, "/" + thumbnail_directory):
            self.__send_200_response('image/png')
            self.wfile.write(read_file_bytes(unquote(self.path)))

        elif str.startswith(self.path, "/?search="):
            self.__send_200_response('text/html')

            search_query_list = unquote(self.path.split('=')[1]).split("+")
            search_query = " ".join(search_query_list)
            search_query_list = [query.lower() for query in search_query_list]

            media = media_manager.search(search_query_list)

            html_code = web_generator.generate_search_page(media, search_query)
            self.wfile.write(bytes(html_code, 'UTF-8'))

        elif self.path == "/all":
            self.__send_200_response('text/html')
            html_code = web_generator.generate_all_page(media_manager.get_all_media(), media_manager.get_albums())
            self.wfile.write(bytes(html_code, 'UTF-8'))

        elif str.startswith(self.path, "/all?search=") and len(self.path) > len("/all?search="):
            self.__send_200_response('text/html')

            search_query_list = unquote(self.path.split('=')[1]).split("+")
            search_query = " ".join(search_query_list)
            search_query_list = [query.lower() for query in search_query_list]

            media = media_manager.search_all(search_query_list)

            html_code = web_generator.generate_all_page(media, media_manager.get_albums(), search_query)
            self.wfile.write(bytes(html_code, 'UTF-8'))

        else:
            self.__send_200_response('text/html')
            html_code = web_generator.generate_index()
            self.wfile.write(bytes(html_code, 'UTF-8'))

    def __send_200_response(self, content_type):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def __send_404_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        self.wfile.write("404")

    def log_message(self, format, *args):
        return


def read_file_bytes(file_path: str) -> bytes:
    with open(os.getcwd() + file_path, 'rb') as file:
        return file.read()
