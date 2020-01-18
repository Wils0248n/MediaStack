import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
from WebGenerator import WebGenerator
from MediaManager import MediaManager

media_manager = MediaManager()


class PhotoStackHTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        if self.path == "/style.css":
            self.send_200_response('text/css')
            self.wfile.write(read_file_bytes("/style.css"))

        elif str.startswith(self.path, "/image"):
            self.send_200_response('text/html')
            media_hash = self.path.split('=')[1]
            html_code = WebGenerator().generate_media_page(media_manager.get_media(media_hash))
            self.wfile.write(bytes(html_code, 'UTF-8'))

        elif str.startswith(self.path, "/photos") or str.startswith(self.path, "/thumbs"):
            self.send_200_response('image/png')
            self.wfile.write(read_file_bytes(unquote(self.path)))

        elif str.startswith(self.path, "/?search") and len(self.path) > 9:
            self.send_200_response('text/html')

            search_query = self.path.split('=')[1].split("+")
            search_query = [unquote(query).replace('_', ' ').lower() for query in search_query]

            media = media_manager.search(search_query)

            html_code = WebGenerator().generate_index(media)
            self.wfile.write(bytes(html_code, 'UTF-8'))

        else:
            self.send_200_response('text/html')
            html_code = WebGenerator().generate_index(media_manager.media_list)
            self.wfile.write(bytes(html_code, 'UTF-8'))

    def send_200_response(self, content_type):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()


def run_web_server(server_class=HTTPServer, handler_class=PhotoStackHTTPHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
    print("Starting Web server...")
    try:
        run_web_server()
    except KeyboardInterrupt:
        print("Exitting...")


def read_file_bytes(file_path):
    with open(os.getcwd() + file_path, 'rb') as file:
        return file.read()


if __name__ == '__main__':
    main()
