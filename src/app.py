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
        'image_urls': store.get_thumbmail_urls(),
        'image_height': settings.THUMBNAIL_HEIGHT,
    }

    return render_template('index.html', **context)


@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')


@app.route('/api/sign', methods=['GET'])
def sign_upload_api():
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    
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
    signature_data = store.sign_image_upload(filename, file_type)

    return json.dumps({
        'data': signature_data['data'],
        'url': signature_data['url']
    })
