from web import MediaStackHTTPHandler
from http.server import HTTPServer


def main():
    print("Starting Web server...")
    try:
        HTTPServer(('', 8001), MediaStackHTTPHandler).serve_forever()
    except KeyboardInterrupt:
        print("Exitting...")


if __name__ == '__main__':
    main()
