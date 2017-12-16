import json

import boto3
from flask import Flask, request, render_template
from slugify import slugify

import settings
import store
from utils import split_file_extension

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
    context = {
        'thumbnails': store.get_thumbnails(),
    }

    return render_template('index.html', **context)


@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')


@app.route('/album', methods=['GET'])
def album_create_page():
    return render_template('create_album.html')


@app.route('/api/album', methods=['POST'])
def album_create_api():
    name = request.args.get('name')

    if not name:
        return 'Album name must not be blank', 400

    # TODO: Validate / clean name

    existing_album = store.get_album(name)
    if existing_album:
        return json.dumps({
            'name': name,
            'slug': slug,
            'created': False
        })
    else:
        slug = slugify(name)
        store.add_album(name, slug)
        return json.dumps({
            'name': name,
            'slug': slug,
            'created': True
        })


@app.route('/api/sign', methods=['GET'])
def sign_upload_api():
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    tags = request.args.get('tags').split(',')  # comma separated list

    if not file_name:
        app.logger.debug('File has no name: %s', file_name)
        return 'File has no name', 400

    base_name, file_extension = split_file_extension(file_name)

    if not file_extension.lower() in settings.ALLOWED_EXTENSIONS:
        app.logger.debug('File has invalid extension: %s', file_name)
        return 'Invalid file type', 400

    if not file_type in settings.ALLOWED_CONTENT_TYPES:
        app.logger.debug('File has invalid content type: %s', file_type)
        return 'Invalid file type', 400

    filename = '.'.join((slugify(base_name), file_extension.lower()))
    signature_data = store.sign_image_upload(filename, file_type, tags)

    return json.dumps({
        'data': signature_data['data'],
        'url': signature_data['url']
    })
