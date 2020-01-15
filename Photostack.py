import os
from WebGenerator import webgenerator
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
from IOManager import readFileBytes
from DatabaseManager import databaseManager

dbManager = databaseManager("photos")
webGenerator = webgenerator()

class PhotoStackHandler(BaseHTTPRequestHandler):
    def __init__(self,request,client_address,server):
        BaseHTTPRequestHandler.__init__(self,request,client_address,server)

    def do_GET(self):
        if self.path == "/style.css":
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(readFileBytes("/style.css"))
        elif str.startswith(self.path, "/photos") or str.startswith(self.path, "/thumbs"):
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(readFileBytes(unquote(self.path)))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(webGenerator.generate(dbManager.getAllImageData()), 'UTF-8'))

def runWebServer(server_class=HTTPServer, handler_class=PhotoStackHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def main():
    print("Starting Webserver...")
    runWebServer()

if __name__ == '__main__':
    main()
