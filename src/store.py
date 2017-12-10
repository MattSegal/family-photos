"""
External datastores
"""
import logging

import boto3

import settings
from utils import get_s3_url, download_file_s3, upload_file_s3

log = logging.getLogger(__name__)
orig_bucket = boto3.resource('s3').Bucket(settings.ORIG_BUCKET_NAME)
thumb_bucket = boto3.resource('s3').Bucket(settings.THUMB_BUCKET_NAME)


def get_thumbmail_urls():
    return (
        get_s3_url(img.key, thumb_bucket) for img in 
        get_thumbnail_images()
    )


def get_thumbnail_images():
    return (
        img for img in thumb_bucket.objects.filter(Prefix='thumbnail/')
        if img.key != 'thumbnail/'
    )


def get_original_image(filename):
    key = 'original/{}'.format(filename)
    return download_file_s3(key, orig_bucket)


def save_thumbnail_image(filename, file):
    upload_file_s3(
       filename=filename,
       path='thumbnail',
       file_obj=file,
       bucket=thumb_bucket
    )


def save_display_image(filename, file):
    upload_file_s3(
       filename=filename,
       path='display',
       file_obj=file,
       bucket=thumb_bucket
    )


def sign_image_upload(filename, file_type):
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
    return {
        'data': presigned_post,
        'url': 'https://{}.s3-ap-southeast-2.amazonaws.com/'.format(orig_bucket.name)
    }
