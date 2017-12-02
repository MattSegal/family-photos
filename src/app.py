import gzip
import os
import sys
import logging

from io import BytesIO

import boto3
from flask import Flask, request, render_template
from PIL import Image, ExifTags
from slugify import slugify
from zappa.async import task

from utils import (
    get_s3_url, gunzip_file, download_file_s3, split_file_extension, upload_file_s3
)


PHOTO_BUCKET_NAME = os.environ['PHOTO_BUCKET_NAME']
WEBSITE_BUCKET_NAME = os.environ['WEBSITE_BUCKET_NAME']
ALLOWED_EXTENSIONS = ('jpeg', 'jpg')


app = Flask(__name__)
photo_bucket = boto3.resource('s3').Bucket(PHOTO_BUCKET_NAME)
website_bucket = boto3.resource('s3').Bucket(WEBSITE_BUCKET_NAME)
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log.debug('Using bucket %s', PHOTO_BUCKET_NAME)
# Maybe use flask-cors
# https://github.com/corydolphin/flask-cors


@app.route('/', methods=['POST'])
def upload():
    # Validate file and filename
    if 'file' not in request.files:
        log.debug('Request did not contain valid file: %s', request.files)
        return 'Request must contain a valid file', 400

    file = request.files['file']
    if not file.filename:
        log.debug('File has no filename: %s', file)
        return 'No file uploaded', 400

    base_name, file_extension = split_file_extension(file.filename)
    if not file_extension in ALLOWED_EXTENSIONS:
        log.debug('File has invalid extension: %s', file)
        return 'Invalid file type', 400

    filename = slugify(base_name) + '.' + file_extension

    # Upload file to S3 bucket
    # upload_file_s3(
    #     filename=filename,
    #     path='original',
    #     file_obj=file,
    #     bucket=photo_bucket
    # )

    resize_image(filename)
    return 'success', 200

@task
def resize_image(filename):
    log.debug('Resizing image %s', filename)
    # Read image into memory from S3
    key = 'original/{}'.format(filename)
    file_obj = download_file_s3(key, photo_bucket)

    # Thumbnail the image and upload to S3
    thumbnail_height = 140  # px
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

    img.thumbnail((sys.maxint, thumbnail_height), Image.ANTIALIAS)
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
        '<img height="{}px" src="{}" />'.format(thumbnail_height, url) 
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
