from typing import Dict
from http.server import BaseHTTPRequestHandler
from urllib import parse
from web.RequestHandler import RequestHandler

request_handler = RequestHandler()


class MediaStackHTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        parsed_url = parse.urlsplit(self.path)
        request = {}
        request["page"] = parsed_url.path
        request["queries"] = parse.parse_qs(parsed_url.query)

        response = request_handler.handle_get_request(request)
        if response[1] is None:
            self._send_404_response()
            self.wfile.write(bytes("404", "UTF-8"))
        else:
            self._send_200_response(response[0])
            self.wfile.write(response[1])

    def do_POST(self):
        parsed_url = parse.urlsplit(self.path)
        request = {}
        request["action"] = parsed_url.path[1:]

        content_length = int(self.headers['Content-Length'])
        post_data = str(self.rfile.read(content_length), "UTF-8")
        request["post"] = self._parse_post_data(post_data)

        response = request_handler.handle_post_request(request)
        if response[1] is None:
            self._send_500_response()
            self.wfile.write(bytes("500", "UTF-8"))
        else:
            self._send_200_response(response[0])
            self.wfile.write(response[1]) 

    def _parse_post_data(self, post_data: str) -> Dict:
        post_data = parse.unquote(post_data)
        post_request = {}
        for input in post_data.split("&"):
            input_data = input.split("=")
            post_request[input_data[0]] = input_data[1]
        return post_request

    def _send_200_response(self, content_type):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _send_404_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _send_500_response(self):
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def log_message(self, format, *args):
        return
