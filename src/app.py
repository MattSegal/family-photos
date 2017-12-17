import json
import re
import urlparse

import boto3
from flask import Flask, request, redirect, render_template, session, url_for
from slugify import slugify

import settings
import store
from utils import split_file_extension

app = Flask(__name__)
app.secret_key = 'change_me_plz'


@app.route('/', methods=['GET'])
def home_page():
    # TODO: query more efficiently
    albums = store.get_albums()
    for album in albums:
        album['url'] = url_for('album_index', slug=album['slug'])
        album['thumbnails'] = store.get_album_thumbnails(album['slug'])[:4]
    context = {
        'albums': [a for a in albums if a['thumbnails']],
    }
    return render_template('index.html', **context)


@app.route('/upload', methods=['GET'])
def upload_page():
    # TODO: CSRF
    context = {
        'albums': store.get_albums() 
    }
    return render_template('upload.html', **context)


@app.route('/album', methods=['GET'])
def album_create_page():
    # TODO: CSRF
    album_data = session.get('album', {})
    context = {
        'album_name': album_data.pop('name', None),
        'album_message': album_data.pop('message', None),
        'album_url': album_data.pop('url', None),
    }
    session['album'] = {}
    return render_template('create_album.html', **context)


@app.route('/album/<slug>', methods=['GET'])
def album_index(slug):
    album = store.get_album(slug) 
    if not album:
        return 'Album {} does not exist.'.format(slug), 404
    
    context = {
        'name': album['name'],
        'thumbnails': store.get_album_thumbnails(slug),
    }
    return render_template('album_index.html', **context)


@app.route('/api/album', methods=['POST'])
def album_create_api():
    post_data = dict(urlparse.parse_qsl(request.get_data()))
    try:
        name = post_data['name']    
    except KeyError:
        return 'Request must contain \'name\' parameter', 400

    # Validate and clean
    name = name.strip(' ')
    validation_regex = r'[\w\s]{3,20}'
    match = re.match(validation_regex, name)
    if not match:
        session['album'] = {
            'message': 'Album name must be 3 to 20 characters, letters and numbers only.'
        }
        return redirect(url_for('album_create_page'))

    name = match.group()
    name = ' '.join([s.capitalize() for s in name.split(' ')])
    slug = slugify(name)

    existing_album = store.get_album(slug)
    if existing_album:
        session['album'] = {
            'name': existing_album['name'],
            'url': url_for('album_index', slug=existing_album['slug']),
            'message': 'An album with that name already exists.'
        }
    else:
        store.add_album(slug, name)
        session['album'] = {
            'name': name,
            'url': url_for('album_index', slug=slug),
            'message': 'New album created.'
        }
    return redirect(url_for('album_create_page'))


@app.route('/api/sign', methods=['GET'])
def sign_upload_api():
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    album_slug = request.args.get('album_slug')

    if not file_name:
        app.logger.debug('File has no name: %s', file_name)
        return 'File has no name', 400

    if not album_slug:
        app.logger.debug('File has no album: %s', album_slug)
        return 'File has no album', 400
    elif not store.get_album(album_slug):
        app.logger.debug('Album does not exist: %s', album_slug)
        return 'Album does not exist: %s', 400

    base_name, file_extension = split_file_extension(file_name)

    if not file_extension.lower() in settings.ALLOWED_EXTENSIONS:
        app.logger.debug('File has invalid extension: %s', file_name)
        return 'Invalid file type', 400

    if not file_type in settings.ALLOWED_CONTENT_TYPES:
        app.logger.debug('File has invalid content type: %s', file_type)
        return 'Invalid file type', 400

    filename = '.'.join((slugify(base_name), file_extension.lower()))
    
    # if store.get_image(filename):
        # return 'Filename already exists - use a different filename', 400

    signature_data = store.sign_image_upload(filename, file_type, album_slug)

    return json.dumps({
        'data': signature_data['data'],
        'url': signature_data['url']
    })
