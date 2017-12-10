import logging
import sys
from io import BytesIO

from PIL import Image, ExifTags

import settings
import store

ORIENTATION_CODE = next(k for k in ExifTags.TAGS.keys() if ExifTags.TAGS[k] == 'Orientation')
log = logging.getLogger(__name__)


def resize_image(filename):
    """
    Download original image from S3, thumbnail it, and upload thumbnail
    """
    log.debug('Resizing image %s', filename)
    img_file = store.get_original_image(filename)

    # Thumbnail the image and upload to S3
    thumb_file, width = set_image_height(img_file, settings.THUMBNAIL_HEIGHT)
    store.save_thumbnail_image(
        filename, thumb_file,
        width=width,
        height=settings.THUMBNAIL_HEIGHT
    )

    # Make a display size image and upload to S3
    disp_file, _ = set_image_height(img_file, settings.DISPLAY_HEIGHT)
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
    return img_bytes, img.width


def ensure_image_upright(img_file):
    """
    Returns img_file, rotated so that it is the right way up
    """
    exif = img_file._getexif()
    if not exif:
        return img_file

    exif = dict(exif.items())
    orientation_num = exif.get(ORIENTATION_CODE)
    if not orientation_num:
        return img_file

    if orientation_num == 3:
        return img_file.rotate(180, expand=True)
    elif orientation_num == 6:
        return img_file.rotate(270, expand=True)
    elif orientation_num == 8:
        return img_file.rotate(90, expand=True)
    else:
        return img_file

def resize_images():
    """
    Utility function to go back and resize everything
    """
    filenames = store.get_original_image_filenames()
    for filename in filenames:
        print('Resizing', filename)
        resize_image(filename)