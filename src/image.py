import logging
import sys
from io import BytesIO

from PIL import Image, ExifTags

import settings
import store

ORIENTATION = next(k for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'Orientation')
log = logging.getLogger(__name__)


def resize_image(filename):
    """
    Download original image from S3, thumbnail it, and upload thumbnail
    """
    log.debug('Resizing image %s', filename)
    img_file = store.get_original_image(filename)

    # Thumbnail the image and upload to S3
    thumb_file = set_image_height(img_file, settings.THUMBNAIL_HEIGHT)
    store.save_thumbnail_image(filename, thumb_file)

    # Make a display size image and upload to S3
    disp_file = set_image_height(img_file, settings.DISPLAY_HEIGHT)
    store.save_display_image(filename, disp_file)


def set_image_height(img_file, height):
    """
    Returns a copy of img_file, thumbnailed to the
    specified height, in pixels
    """
    img = Image.open(img_file)
    img = ensure_image_upright(img)
    img.thumbnail((sys.maxint, height), Image.ANTIALIAS)
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


def ensure_image_upright(img_file):
    """
    Returns a copy of img_file,
    with rotated so that it is the right way up
    """
    exif = img_file._getexif()
    if not exif:
        return img_file

    exif = dict(exif.items())

    if exif[ORIENTATION] == 3:
        return img_file.rotate(180, expand=True)
    elif exif[ORIENTATION] == 6:
        return img_file.rotate(270, expand=True)
    elif exif[ORIENTATION] == 8:
        return img_file.rotate(90, expand=True)
    else:
        return img_file
