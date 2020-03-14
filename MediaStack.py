import logging
from jinja2 import Template
from flask import Flask, render_template, url_for, request, redirect, send_file
from mediastack.controller.MediaManager import MediaManager
from mediastack.controller.MediaManager import MediaSet

logging.getLogger('iptcinfo').setLevel(logging.ERROR)

flask = Flask("Test", template_folder="mediastack/web/pages", static_folder="mediastack/web")
media_manager = MediaManager()

@flask.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@flask.route('/mediapage', methods=['GET', 'POST'])
def media_page():
    if request.args.get('hash') is not None:
        media = media_manager.find_media(request.args.get('hash'))
        if request.method == 'POST':
            _handle_post_request(media, request.form)
        return render_template('media.html', 
            media=media, 
            edit=(request.args.get('edit') is not None), 
            set=media_manager.find_media_set(request.args.get('set')).value)

@flask.route('/searchpage', methods=['GET'])
def search_page():
    media_set = request.args.get('set')
    search = request.args.get('search')
    if search is not None:
        search = search.split(' ')
    return render_template('thumbnails.html', 
    media_list=media_manager.search(media_set, search), 
    set=media_manager.find_media_set(request.args.get('set')).value)

@flask.route('/thumbs/<string:hash>', methods=['GET'])
def thumbnail_file(hash):
    return send_file('thumbs/' + hash, mimetype='image/gif')

@flask.route('/media/<path:path>', methods=['GET'])
def media_file(path):
    return send_file('media/' + path, mimetype='')

def _handle_post_request(media, forms_data):
    if forms_data is None or media is None:
        return
    elif "add_tag" in forms_data.keys():
        media_manager.add_tag(media, forms_data['add_tag'])
    elif "rating" in forms_data.keys():
        media_manager.change_score(media, forms_data['rating'])
    elif "source" in forms_data.keys():
        media_manager.change_source(media, forms_data['source'])
    else:
        media_manager.remove_tag(media, next(forms_data.keys()))

def main():
    #flask.run(host='192.168.42.31')
    flask.run()

if __name__ == '__main__':
    main()
