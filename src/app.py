import json

import boto3
from flask import Flask, request, render_template
from slugify import slugify

import settings
from utils import get_s3_url, split_file_extension

app = Flask(__name__)
orig_bucket = boto3.resource('s3').Bucket(settings.ORIG_BUCKET_NAME)
thumb_bucket = boto3.resource('s3').Bucket(settings.THUMB_BUCKET_NAME)

@app.route('/', methods=['GET'])
def home_page():
    image_urls = (
        get_s3_url(img.key, thumb_bucket) for img in
        thumb_bucket.objects.filter(Prefix='thumbnail/') if img.key != 'thumbnail/'
    )

    context = {
        'image_urls': image_urls,
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
    
    key = 'original/{}.{}'.format(slugify(base_name), file_extension.lower())

    app.logger.debug('Signing upload to %s', key)
    presigned_post = orig_bucket.meta.client.generate_presigned_post(
        Bucket=orig_bucket.name,
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
        'url': 'https://{}.s3-ap-southeast-2.amazonaws.com/'.format(orig_bucket.name)
    })
