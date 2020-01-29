from http.server import BaseHTTPRequestHandler
from web.QueryHandler import QueryHandler

query_handler = QueryHandler()


class MediaStackHTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        response = query_handler.handle_get_request(self.path)
        if response[1] is None:
            self.__send_404_response()
            self.wfile.write(bytes("404", "UTF-8"))
        else:
            self.__send_200_response(response[0])
            self.wfile.write(response[1])

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = str(self.rfile.read(content_length), "UTF-8").split("=")

        response = query_handler.handle_post_request(self.path, post_data)
        if response[1] is None:
            self.__send_500_response()
            self.wfile.write(bytes("500", "UTF-8"))
        else:
            self.__send_200_response(response[0])
            self.wfile.write(response[1])

    def __send_200_response(self, content_type):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def __send_404_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def __send_500_response(self):
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args):
        return
