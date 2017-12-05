import gzip
import os
import sys
import logging
import json
from io import BytesIO
from urlparse import urljoin

from cloudinary.uploader import upload
from flask import Flask, request, render_template

import settings
from utils import split_file_extension


app = Flask(__name__)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

@app.route('/', methods=['GET'])
def home_page():
    url = urljoin(settings.CLOUDINARY_URL, 'resources/image')
    headers = {
        'Authorization': settings.CLOUDINARY_AUTH
    }
    import requests
    r = requests.get(url, headers=headers)
    r.raise_for_status()


    image_urls = [
        img['secure_url'].replace('v1512474005', 'h_140') 
        for img in  r.json()['resources']
    ]
    
    context = {
        'image_urls': image_urls,
        'image_height': settings.THUMBNAIL_HEIGHT,
    }

    return render_template('index.html', **context)


@app.route('/upload', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/api/upload', methods=['POST'])
def upload_api():
    # Validate file and filename
    if 'file' not in request.files:
        log.debug('Request did not contain valid file: %s', request.files)
        return 'Request must contain a valid file', 400

    file = request.files['file']
    if not file.filename:
        log.debug('File has no filename: %s', file)
        return 'No file uploaded', 400

    base_name, file_extension = split_file_extension(file.filename)
    if not file_extension.lower() in settings.ALLOWED_EXTENSIONS:
        log.debug('File has invalid extension: %s', file)
        return 'Invalid file type', 400

    upload_result = upload(file) # tags = xxxx
    log.debug(upload_result)
    return 'success', 200
