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
            self.handle_css_request()

        elif str.startswith(self.path, "/media="):
            self.handle_media_request()

        elif str.startswith(self.path, "/album="):
            self.handle_album_request()

        elif str.startswith(self.path, "/" + media_directory) or str.startswith(self.path, "/" + thumbnail_directory):
            self.handle_media_file_request()

        elif str.startswith(self.path, "/?search="):
            self.handle_search_request()

        elif self.path == "/all":
            self.handle_all_media_request()

        elif str.startswith(self.path, "/all?search=") and len(self.path) > len("/all?search="):
            self.handle_search_all_request()

        else:
            self.handle_default_request()

    def handle_css_request(self):
        self.__send_200_response('text/css')
        self.wfile.write(read_file_bytes("/style.css"))

    def handle_media_request(self):
        self.__send_200_response('text/html')
        media_hash = self.path.split('=')[1]
        html_code = web_generator.generate_media_page(media_manager.find_media(media_hash))
        self.wfile.write(bytes(html_code, 'UTF-8'))

    def handle_album_request(self):
        self.__send_200_response('text/html')
        album_query = self.path.split('=')[1].split('/')
        album_name = unquote(album_query[0])
        if len(album_query) == 2:
            current_index = int(self.path.split('/')[2])
            html_code = web_generator.generate_album_media_page(media_manager.get_albums()[album_name],
                                                                current_index)
        elif len(album_query) == 1:
            html_code = web_generator.generate_album_page(media_manager.get_albums()[album_name])
        self.wfile.write(bytes(html_code, 'UTF-8'))

    def handle_media_file_request(self):
        self.__send_200_response('image/png')
        self.wfile.write(read_file_bytes(unquote(self.path)))

    def handle_search_request(self):
        self.__send_200_response('text/html')
        search_query_list = unquote(self.path.split('=')[1]).split("+")
        search_query = " ".join(search_query_list)
        search_query_list = [query.lower() for query in search_query_list]
        media = media_manager.search(search_query_list)
        html_code = web_generator.generate_search_page(media, search_query)
        self.wfile.write(bytes(html_code, 'UTF-8'))

    def handle_default_request(self):
        self.__send_200_response('text/html')
        html_code = web_generator.generate_index()
        self.wfile.write(bytes(html_code, 'UTF-8'))

    def handle_all_media_request(self):
        self.__send_200_response('text/html')
        html_code = web_generator.generate_all_page(media_manager.get_all_media(), media_manager.get_albums())
        self.wfile.write(bytes(html_code, 'UTF-8'))

    def handle_search_all_request(self):
        self.__send_200_response('text/html')
        search_query_list = unquote(self.path.split('=')[1]).split("+")
        search_query = " ".join(search_query_list)
        search_query_list = [query.lower() for query in search_query_list]
        media = media_manager.search_all(search_query_list)
        html_code = web_generator.generate_all_page(media, media_manager.get_albums(), search_query)
        self.wfile.write(bytes(html_code, 'UTF-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = str(self.rfile.read(content_length), "UTF-8").split("=")
        if post_data[0] == "add_tag":
            if str.startswith(self.path, "/media"):
                media = media_manager.find_media(self.path.split('=')[1])
                media.tags.append(post_data[1])
                media_manager.update_media_tags(media)
                self.handle_media_request()
            elif str.startswith(self.path, "/album"):
                album_query = self.path.split('=')[1].split('/')
                album_name = unquote(album_query[0])
                current_index = int(self.path.split('/')[2])
                media = media_manager.get_albums()[album_name].media_list[current_index]
                media.tags.append(post_data[1])
                media_manager.update_media_tags(media)
                self.handle_album_request()
        else:
            self.handle_default_request()

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
