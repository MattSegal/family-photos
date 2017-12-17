import logging
import time
import sys
from datetime import datetime
from io import BytesIO

from PIL import Image, ExifTags

import settings
import store

ORIENTATION_CODE = next(k for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'Orientation')
DATETIME_CODE = next(k for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'DateTime')

log = logging.getLogger(__name__)


def resize_image(filename):
    """
    Download original image from S3, thumbnail it, and upload thumbnail
    """
    log.debug('Resizing image %s', filename)
    img_file = store.get_original_image(filename)

    # Thumbnail the image and upload to S3
    taken_time = get_image_taken_time(img_file)
    thumb_file = set_image_size(img_file,
        width=settings.THUMBNAIL_WIDTH,
        height=settings.THUMBNAIL_HEIGHT
    )
    store.save_thumbnail_image(filename, thumb_file,
        width=settings.THUMBNAIL_WIDTH,
        height=settings.THUMBNAIL_HEIGHT,
        taken_time=taken_time
    )

    # Make a display size image and upload to S3
    disp_file, _ = set_image_height(img_file,
        height=settings.DISPLAY_HEIGHT
    )
    store.save_display_image(filename, disp_file)


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
    img.thumbnail((sys.maxint, height), Image.ANTIALIAS)
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

    # '2017:09:03 13:41:35'
    dt = datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
    return int(time.mktime(dt.timetuple()))

def resize_images():
    """
    Utility function to go back and resize everything
    """
    filenames = store.get_original_image_filenames()
    for filename in filenames:
        print('Resizing', filename)
        resize_image(filename)
