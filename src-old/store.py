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


def get_album(slug):
    resp = albums_table.get_item(Key={'slug': slug})
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
    return resp.get('Item')


def get_albums():
    return sorted(albums_table.scan()['Items'], key=lambda img: img['name'])


def add_album(slug, name):
    albums_table.put_item(Item={
        'slug': slug,
        'name': name,
        'created': int(time.time() * 1000),
    })


def get_thumbnails():
    # UNUSED
    return sorted(images_table.scan()['Items'], key=lambda img: img['created'])


def get_album_thumbnails(album_slug):
    """
    TODO - query DynamoDB more efficiently
    """
    thumbs = (
        img for img in images_table.scan()['Items']
        if img['album_slug'] == album_slug and
        img.get('taken')
    ) 
    return sorted(thumbs, key=lambda img: img['taken'])


def get_image(filename):
    resp = images_table.get_item(Key={'filename': filename})
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
    return resp.get('Item')

def delete_image(filename):
    # Delete from DynamoDB
    resp = images_table.delete_item(Key={'filename': filename})
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200

    # Delete from thumbnails
    delete = {'Objects': [
        {'Key': 'display/' + filename},
        {'Key': 'thumbnail/' + filename}
    ]}
    resp = thumb_bucket.delete_objects(Delete=delete)
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200

    # Delete from original bucket
    delete = {'Objects': [{'Key': 'original/' + filename}]}
    resp = orig_bucket.delete_objects(Delete=delete)
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200


def get_original_image(filename):
    key = 'original/{}'.format(filename)
    return download_file_s3(key, orig_bucket)


def get_original_image_filenames():
    return (
        img.key.split('/')[-1]
        for img in orig_bucket.objects.filter(Prefix='original/')
        if img.key != 'original/'
    )

def save_thumbnail_image(filename, file, width, height, taken_time):
    upload_file_s3(
       filename, file,
       path='thumbnail',
       bucket=thumb_bucket
    )
    key = 'thumbnail/{}'.format(filename)
    images_table.update_item(
        Key={'filename': filename},
        UpdateExpression=(
            'SET thumb_url = :t,'
            'width = :w,'
            'height = :h,'
            'created = :ct,'
            'taken = :tt'
        ),
        ExpressionAttributeValues={
            ':t': get_s3_url(key, thumb_bucket),
            ':w': width,
            ':h': height,
            ':ct': int(time.time() * 1000),
            ':tt': taken_time
        }
    )


def save_display_image(filename, file):
    upload_file_s3(
       filename, file,
       path='display',
       bucket=thumb_bucket
    )


def sign_image_upload(filename, file_type, album_slug):
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
    resp = images_table.put_item(Item={
        'filename': filename,
        'album_slug': album_slug
    })
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
    return {
        'data': presigned_post,
        'url': 'https://{}.s3-ap-southeast-2.amazonaws.com/'.format(orig_bucket.name)
    }
