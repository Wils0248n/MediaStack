import logging
from jinja2 import Template
from flask import Flask, render_template, url_for, request, redirect, send_file
from mediastack.controller.MediaManager import MediaManager
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
        media_list = media_manager.search_all(request.args.get('search').split(' '))
        return render_template('thumbnails.html', media_list=media_list)
    return render_template('thumbnails.html', media_list=media_manager.get_all_media())

@flask.route('/media', methods=['GET'])
def media_page():
    if request.args.get('search') is not None:
        media_list = media_manager.search(request.args.get('search').split(' '))
        return render_template('thumbnails.html', media_list=media_list)
    if request.args.get('hash') is not None:
        media = media_manager.find_media(request.args.get('hash'))
        return render_template('media.html', media=media,
            album_length=media_manager.count_media_in_album(media.album_name),
            next_index=determine_next_index(media), 
            previous_index=determine_previous_index(media))
    if request.args.get('index') is not None:
        media = media_manager.find_media_by_album(request.args.get('album'), int(request.args.get('index')))
        return render_template('media.html', media=media, 
            album_length=media_manager.count_media_in_album(media.album_name),
            next_index=determine_next_index(media), 
            previous_index=determine_previous_index(media))
    return render_template('thumbnails.html', media_list=media_manager.get_media())

def determine_next_index(media: Media) -> int:
    if media.album is None:
        return 0
    album_length = media_manager.count_media_in_album(media.album_name)
    if media.album_index + 1 == album_length:
        return 0
    else:
        return media.album_index + 1

def determine_previous_index(media: Media) -> int:
    if media.album is None:
        return 0
    album_length = media_manager.count_media_in_album(media.album_name)
    if media.album_index - 1 < 0:
        return album_length - 1
    else:
        return media.album_index - 1

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
