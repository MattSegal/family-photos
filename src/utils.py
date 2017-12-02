import logging
import gzip
import shutil
import os

from io import BytesIO


DO_NOT_COMPRESS = ('png', 'jpeg', 'jpg', 'gif', 'ico')
CONTENT_TYPES = {
    'html': 'text/html',
    'css': 'text/css',
    'jpeg': 'image/jpeg',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'ico': 'image/x-icon',
    'js': 'application/javascript',
    'json': 'application/json'
}

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def split_file_extension(filename):
    parts = filename.split('.')
    name = '.'.join(parts[:-1])
    ext = parts[-1]
    return name, ext


def get_content_type(filename):
    _, extension = split_file_extension(filename)
    return CONTENT_TYPES.get(extension, 'text/plain')


def upload_file_s3(filename, path, file_obj, bucket):
    key = os.path.join(path, filename).replace('\\', '/')
    content_type = get_content_type(filename)
    log.debug('Uploading %s as %s to %s', key, content_type, bucket.name)

    # Compress the file if it's not an image
    _, file_extension = split_file_extension(filename)
    should_compress = file_extension not in DO_NOT_COMPRESS
    if should_compress:
        log.debug('Compressing %s', key)
        f_compressed = BytesIO()
        with gzip.GzipFile(fileobj=f_compressed, mode='wb') as gz:
            shutil.copyfileobj(file_obj, gz)
        f_compressed.seek(0)
        f_upload = f_compressed
    else:
        f_upload = file_obj

    file_metadata = {
        'ContentType': content_type, 
        'ACL': 'public-read'
    }
    if should_compress:
        file_metadata['ContentEncoding'] = 'gzip'

    bucket.upload_fileobj(f_upload, key, file_metadata)
    log.debug('Finished uploading %s', key)


def download_file_s3(key, bucket):
    file_obj = BytesIO()
    bucket.download_fileobj(key, file_obj)
    file_obj.seek(0)
    return file_obj


def get_s3_url(key, bucket, region='ap-southeast-2'):
    return 'https://s3-{region}.amazonaws.com/{bucket}/{key}'.format(
        region=region,
        bucket=bucket.name,
        key=key
    )


def gunzip_file(file_obj):
    file_obj_uncompressed = BytesIO()
    with gzip.GzipFile(fileobj=file_obj, mode='rb') as gz:
        shutil.copyfileobj(gz, file_obj_uncompressed)
    file_obj_uncompressed.seek(0)
    return file_obj_uncompressed
