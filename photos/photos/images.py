import logging
import os
import hashlib
from datetime import datetime
from io import BytesIO

from django.conf import settings
from django.utils import timezone
from PIL import Image, ExifTags

ORIENTATION_CODE = next(k for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'Orientation')
DATETIME_CODE = next(k for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'DateTime')

log = logging.getLogger(__name__)


def get_local_filename(instance, filename):
    """
    Get local filename for the photo - use a hash of the photo bytes to
    ensure that photos are unique.
    """
    img_bytes = instance.local_file._file.file.read()
    instance.local_file._file.file.seek(0)
    filename = get_img_filename(img_bytes, filename)
    return filename


def get_s3_key(instance, filename):
    """
    Get S3 key for the photo - use a hash of the photo bytes to
    ensure that photos are unique.
    """
    img_bytes = instance.file._file.file.read()
    instance.file._file.file.seek(0)
    filename = get_img_filename(img_bytes, filename)
    return instance.get_original_key(filename)


def get_img_filename(img_bytes, filename):
    """
    Get filename from hash of image
    """
    filename_base = hashlib.md5(img_bytes).hexdigest()
    _, filename_ext = os.path.splitext(filename)
    return filename_base + filename_ext.lower()


def thumbnail(photo):
    """
    Thumbnail photo and upload it to S3
    """
    log.info('Resizing photo %s with file %s', photo.pk, photo.file.name)
    storage = photo.file.storage
    bucket = storage._wrapped._bucket

    with storage.open(photo.file.name, 'rb') as img_file:
        # Thumbnail the image and upload to S3
        taken_time = get_image_taken_time(img_file)
        thumb_file = set_image_size(img_file,
            width=settings.THUMBNAIL_WIDTH,
            height=settings.THUMBNAIL_HEIGHT
        )
        disp_file, _ = set_image_height(img_file,
            height=settings.DISPLAY_HEIGHT
        )

    upload_config = {
        'ContentType': 'image/jpeg',
        'ACL': 'public-read'
    }

    key = photo.get_thumb_key()
    log.info('Uploading %s', key)
    bucket.upload_fileobj(thumb_file, key, upload_config)
    log.info('Finished uploading %s', key)

    key = photo.get_display_key()
    log.info('Uploading %s', key)
    bucket.upload_fileobj(disp_file, key, upload_config)
    log.info('Finished uploading %s', key)

    photo.taken_at = taken_time
    photo.thumbnailed_at = timezone.now()
    photo.save()


def set_image_size(img_file, width, height):
    """
    Resizes the image so that it fills a box of width x height
    returns
        a resized copy of img_file
    """
    img = Image.open(img_file)
    img = ensure_image_upright(img)

    original_aspect_ratio = float(img.width) / img.height
    crop_aspect_ratio = float(width) / height
    if crop_aspect_ratio > original_aspect_ratio:
        # Crop height of image to fit new AR
        new_height = img.width / crop_aspect_ratio
        img = img.crop((
            # left, upper, right, lower
            0,
            0.5 * img.height - 0.5 * new_height,
            img.width,
            0.5 * img.height + 0.5 * new_height
        ))
    else:
        # Crop width of image to fit new AR
        new_width = img.height * crop_aspect_ratio
        img = img.crop((
            0.5 * img.width - 0.5 * new_width,
            0,
            0.5 * img.width + 0.5 * new_width,
            img.height
        ))

    img.thumbnail((width, height), Image.ANTIALIAS)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def set_image_height(img_file, height):
    """
    Resizes the image so that it has specified height
    while maintaining its aspect ratio
    returns
        a resized copy of img_file
        width in px
    """
    img = Image.open(img_file)
    img = ensure_image_upright(img)
    img.thumbnail((float("inf"), height), Image.ANTIALIAS)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes, img.width


def ensure_image_upright(img):
    """
    Returns img, rotated so that it is the right way up
    """
    exif = img._getexif()
    if not exif:
        return img

    exif = dict(exif.items())
    orientation_num = exif.get(ORIENTATION_CODE)
    if not orientation_num:
        return img

    if orientation_num == 3:
        return img.rotate(180, expand=True)
    elif orientation_num == 6:
        return img.rotate(270, expand=True)
    elif orientation_num == 8:
        return img.rotate(90, expand=True)
    else:
        return img


def get_image_taken_time(img_file):
    """
    Reads a time int (epoch ms) from img EXIF data
    """
    img = Image.open(img_file)
    exif = img._getexif()
    if not exif:
        datetime_str = '2100:01:01 01:01:01'
    else:
        exif = dict(exif.items())
        datetime_str = exif.get(DATETIME_CODE)
        if not datetime_str:
            datetime_str = '2100:01:01 01:01:01'

    return datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
