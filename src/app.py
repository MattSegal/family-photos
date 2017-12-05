import gzip
import os
import sys
import logging
import json

from io import BytesIO

import boto3

from cloudinary.uploader import upload

from flask import Flask, request, render_template
# from flask_s3 import FlaskS3 # TODO or remove dependency
# http://flask-s3.readthedocs.io/en/latest/
# from PIL import Image, ExifTags
from slugify import slugify
from zappa.async import task

import settings
from utils import (
    get_s3_url, gunzip_file, download_file_s3, split_file_extension, upload_file_s3
)


app = Flask(__name__)
photo_bucket = boto3.resource('s3').Bucket(settings.PHOTO_BUCKET_NAME)
website_bucket = boto3.resource('s3').Bucket(settings.WEBSITE_BUCKET_NAME)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log.debug('Using bucket %s', settings.PHOTO_BUCKET_NAME)
# Maybe use flask-cors - https://github.com/corydolphin/flask-cors

@app.route('/', methods=['GET'])
def home_page():
    image_urls = (
        get_s3_url(img.key, photo_bucket) for img in
        photo_bucket.objects.filter(Prefix='thumbnail/') if img.key != 'thumbnail/'
    )

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

@app.route('/api/sign', methods=['GET'])
def sign_upload_api():
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')
    
    if not file_name:
        log.debug('File has no name: %s', file_name)
        return 'File has no name', 400

    base_name, file_extension = split_file_extension(file_name)

    if not file_extension.lower() in settings.ALLOWED_EXTENSIONS:
        log.debug('File has invalid extension: %s', file_name)
        return 'Invalid file type', 400

    if not file_type in settings.ALLOWED_CONTENT_TYPES:
        log.debug('File has invalid content type: %s', file_type)
        return 'Invalid file type', 400
    
    key = 'original/{}.{}'.format(slugify(base_name), file_extension.lower())

    presigned_post = photo_bucket.meta.client.generate_presigned_post(
        Bucket=photo_bucket.name,
        Key=key,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
          {"acl": "public-read"},
          {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://{}.s3.amazonaws.com/{}'.format(photo_bucket.name, key)
    })


# TODO: https://github.com/Miserlou/Zappa#executing-in-response-to-aws-events
@task
def resize_image(filename):
    log.debug('Resizing image %s', filename)
    # Read image into memory from S3
    key = 'original/{}'.format(filename)
    file_obj = download_file_s3(key, photo_bucket)

    # Thumbnail the image and upload to S3
    
    img = Image.open(file_obj)
    # Account for rotated image
    for key in ExifTags.TAGS.keys(): 
        if ExifTags.TAGS[key] == 'Orientation': 
            orientation = key
            break 

    exif = dict(img._getexif().items())
    if exif[orientation] == 3: 
        img=img.rotate(180, expand=True)
    elif exif[orientation] == 6: 
        img=img.rotate(270, expand=True)
    elif exif[orientation] == 8: 
        img=img.rotate(90, expand=True)

    img.thumbnail((sys.maxint, settings.THUMBNAIL_HEIGHT), Image.ANTIALIAS)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    upload_file_s3(
        filename=filename,
        path='thumbnail',
        file_obj=img_bytes,
        bucket=photo_bucket
    )

    image_urls = (
        get_s3_url(img.key, photo_bucket) for img in
        photo_bucket.objects.filter(Prefix='thumbnail/') if img.key != 'thumbnail/'
    )
    image_tag_list = ''.join(
        '<img height="{}px" src="{}" />'.format(settings.THUMBNAIL_HEIGHT, url) 
        for url in image_urls
    )
    # Read layout html, which happens to be compressed
    file_obj = download_file_s3('_index.html', website_bucket)
    file_obj = gunzip_file(file_obj)
    file_html = file_obj.read()

    file_html = file_html.format(images=image_tag_list)

    upload_file_s3(
        filename='index.html',
        path='',
        file_obj=BytesIO(file_html),
        bucket=website_bucket
    )
