import logging
from jinja2 import Template
from flask import Flask, render_template, url_for, request, redirect, send_file
from mediastack.controller.MediaManager import MediaManager
from mediastack.controller.MediaManager import MediaSet
from mediastack.model.Media import Media

logging.getLogger('iptcinfo').setLevel(logging.ERROR)

flask = Flask("Test", template_folder="mediastack/web/pages", static_folder="mediastack/web")
media_manager = MediaManager()

@flask.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@flask.route('/all', methods=['GET'])
def all_media_page():
    search = request.args.get('search')
    if search is not None:
        search = search.split(' ')
    return render_template('thumbnails.html', media_list=media_manager.search(MediaSet.ALL, search))

@flask.route('/general', methods=['GET'])
def general_media_page():
    search = request.args.get('search')
    if search is not None:
        search = search.split(' ')
    return render_template('thumbnails.html', media_list=media_manager.search(MediaSet.GENERAL, search))

@flask.route('/media', methods=['GET'])
def media_page():
    if request.args.get('hash') is not None:
        media = media_manager.find_media(request.args.get('hash'))
        return render_template('media.html', media=media)
    return None

@flask.route('/thumbs/<string:hash>', methods=['GET'])
def thumbnail_file(hash):
    return send_file('thumbs/' + hash, mimetype='image/gif')

@flask.route('/media/<path:path>', methods=['GET'])
def media_file(path):
    return send_file('media/' + path, mimetype='')

def main():
    flask.run()

if __name__ == '__main__':
    main()
