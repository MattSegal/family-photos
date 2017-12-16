"""
External datastores:
  - AWS S3
  - AWS DynamoDB
"""
import time
import logging

import boto3

import settings
from utils import get_s3_url, download_file_s3, upload_file_s3

log = logging.getLogger(__name__)
orig_bucket = boto3.resource('s3').Bucket(settings.ORIG_BUCKET_NAME)
thumb_bucket = boto3.resource('s3').Bucket(settings.THUMB_BUCKET_NAME)
images_table = boto3.resource('dynamodb').Table(settings.IMAGE_TABLE_NAME)
albums_table = boto3.resource('dynamodb').Table(settings.ALBUM_TABLE_NAME)


def get_album(name):
    import pdb;pdb.set_trace()
    resp = albums_table.get_item(Key={'name': name})
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
    return resp.get('Item')


def add_album(name, slug):
    albums_table.put_item(Item={
        'name': name,
        'slug': slug,
        'created': int(time.time() * 1000),
    })


def get_thumbnails():
    return images_table.scan()['Items']


def get_original_image(filename):
    key = 'original/{}'.format(filename)
    return download_file_s3(key, orig_bucket)


def get_original_image_filenames():
    return (
        img.key.split('/')[-1]
        for img in orig_bucket.objects.filter(Prefix='original/')
        if img.key != 'original/'
    )


def save_thumbnail_image(filename, file, width, height):
    upload_file_s3(
       filename, file,
       path='thumbnail',
       bucket=thumb_bucket
    )
    key = 'thumbnail/{}'.format(filename)
    images_table.put_item(Item={
        'filename': filename,
        'thumb_url': get_s3_url(key, thumb_bucket),
        'width': width,
        'height': height,
        'created': int(time.time() * 1000),
    })


def save_display_image(filename, file):
    upload_file_s3(
       filename, file,
       path='display',
       bucket=thumb_bucket
    )


def sign_image_upload(filename, file_type, tags):
    key = 'original/' + filename
    log.debug('Signing upload to %s', key)
    presigned_post =  orig_bucket.meta.client.generate_presigned_post(
        Bucket=orig_bucket.name,
        Key=key,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
          {"acl": "public-read"},
          {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )
    images_table.put_item(Item={
        'filename': filename,
        'tags': tags
    })
    return {
        'data': presigned_post,
        'url': 'https://{}.s3-ap-southeast-2.amazonaws.com/'.format(orig_bucket.name)
    }
