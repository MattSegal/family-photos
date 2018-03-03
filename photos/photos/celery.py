import os
from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

from photos.images import thumbnail

app = Celery('photos', broker='amqp://localhost')
app.config_from_object('django.conf:settings', namespace='CELERY')

logging = get_task_logger(__name__)


@app.task
def upload_photo_to_s3(photo_pk):
    """
    Given a photo with a local file on disk, upload it to S3.
    """
    logging.info('Processing Photo[%s]', photo_pk)

    from photos.models import Photo
    photo = Photo.objects.get(pk=photo_pk)
    logging.info('Fetched Photo[%s] as %s', photo_pk, photo)
    if photo.uploaded_at:
        logging.info('Photo[%s] is already uploaded', photo_pk)
        return

    if not photo.local_file:
        msg = 'Cannot upload file to S3 - {} is missing local copy'.format(photo)
        raise ValueError(msg)

    logging.info('Uploading %s original to S3', photo)
    # TODO - stop FS from mangling names
    s3_key = photo.get_original_key(photo.local_file.name)
    s3_storage = photo.file.storage
    fs_storage = photo.local_file.storage
    with fs_storage.open(photo.local_file.name, 'rb') as f:
        with s3_storage.open(s3_key, 'wb') as s3_f:
            s3_f.write(f.read())

    photo.file.name = s3_key
    photo.uploaded_at = timezone.now()
    photo.save()

    logging.info('Deleting local copy %s from %s', photo.local_file, photo)
    photo.local_file.delete()

    logging.info('Finished processing Photo[%s]', photo_pk)
    if not photo.thumbnailed_at:
        thumbnail_photo.delay(photo.pk)


@app.task
def thumbnail_photo(photo_pk):
    """
    Given a photo that has been uploaded to S3,
    create thumbnails and upload them to S3
    """
    logging.info('Thumbnailing a Photo[%s]', photo_pk)
    from photos.models import Photo
    photo = Photo.objects.get(pk=photo_pk)
    logging.info('Fetched Photo[%s] as %s', photo_pk, photo)
    if photo.thumbnailed_at:
        logging.info('Photo[%s] is already thumbnailed', photo_pk)
        return

    thumbnail(photo)
    logging.info('Finished thumbnailing a Photo[%s]', photo_pk)
