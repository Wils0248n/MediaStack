from MediaStackHTTPHandler import MediaStackHTTPHandler
from http.server import HTTPServer


def main():
    print("Starting Web server...")
    try:
        HTTPServer(('', 8000), MediaStackHTTPHandler).serve_forever()
    except KeyboardInterrupt:
        print("Exitting...")


if __name__ == '__main__':
    main()
