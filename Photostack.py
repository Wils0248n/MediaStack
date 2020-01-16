import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
from WebGenerator import webgenerator
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

        elif str.startswith(self.path, "/image"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            imageHash = self.path.split('=')[1]
            imageData = dbManager.getImageDataWithHash(imageHash)
            imageTags = dbManager.getImageTags(imageHash)
            imageMetadata = []

            htmlcode = webGenerator.generateImagePage(imageData, imageTags, imageMetadata)
            self.wfile.write(bytes(htmlcode, 'UTF-8'))

        elif str.startswith(self.path, "/photos") or str.startswith(self.path, "/thumbs"):
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()

            self.wfile.write(readFileBytes(unquote(self.path)))

        elif str.startswith(self.path, "/?search") and len(self.path) > 9:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            searchQuery = self.path.split('=')[1].split("+")
            searchQuery = [unquote(query).replace('_', ' ').lower() for query in searchQuery]
            print(searchQuery)
            htmlcode = webGenerator.generateIndex(dbManager.searchDatabase(searchQuery))
            self.wfile.write(bytes(htmlcode, 'UTF-8'))

        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            htmlcode = webGenerator.generateIndex(dbManager.getAllImageData())
            self.wfile.write(bytes(htmlcode, 'UTF-8'))

def runWebServer(server_class=HTTPServer, handler_class=PhotoStackHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def main():
    print("Starting Webserver...")
    runWebServer()

if __name__ == '__main__':
    main()
