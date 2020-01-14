import os
from WebGenerator import webgenerator
from http.server import BaseHTTPRequestHandler, HTTPServer
from IOManager import readFileBytes

class PhotoStackHandler(BaseHTTPRequestHandler):
    def __init__(self,request,client_address,server):
        BaseHTTPRequestHandler.__init__(self,request,client_address,server)

    def do_GET(self):
        if self.path == "/style.css":
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(readFileBytes("style.css"))
        elif str.startswith(self.path, "/photos") or str.startswith(self.path, "/thumbs"):
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(readFileBytes(self.path))
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(webgenerator().generate(), 'UTF-8'))

def runWebServer(server_class=HTTPServer, handler_class=PhotoStackHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def main():

    runWebServer()

def readFile(filePath):
    with open(os.getcwd() + os.path.sep + filePath) as file:
        return file.read()

def readFileBytes(filePath):
    with open(os.getcwd() + os.path.sep + filePath, 'rb') as file:
        return file.read()

if __name__ == '__main__':
    main()
