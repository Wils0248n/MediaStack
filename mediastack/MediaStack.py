from web.MediaStackHTTPHandler import MediaStackHTTPHandler
from http.server import HTTPServer
import logging

logging.getLogger('iptcinfo').setLevel(logging.ERROR)

def main():
    print("Starting Web server...")
    try:
        HTTPServer(('', 8001), MediaStackHTTPHandler).serve_forever()
    except KeyboardInterrupt:
        print("Exitting...")


if __name__ == '__main__':
    main()
