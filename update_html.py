from __future__ import print_function
import os
import boto3

from src.utils import upload_file_s3

bucket = boto3.resource('s3').Bucket('ms-family-photos-website')

SOURCE_DIR = 'webpage/'


def upload(source_dir=SOURCE_DIR):
    """
    Recursively upload all files in 'source_dir' to an S3 bucket
    """
    folders = (
        os.path.join(source_dir, node) for node in os.listdir(source_dir)
        if os.path.isdir(os.path.join(source_dir, node))
    )

    for folder in folders:
        print('Uploading folder {}'.format(folder))
        upload(folder)

    files = (
        node for node in os.listdir(source_dir)
        if os.path.isfile(os.path.join(source_dir, node))
    )

    for filename in files:
        with open(os.path.join(source_dir, filename), 'rb') as file_obj:
            path = source_dir.replace(SOURCE_DIR, '')
            upload_file_s3(filename, path, file_obj, bucket)

if __name__ == '__main__':
    upload()