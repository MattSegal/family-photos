import logging

from django.utils import timezone
from django_q.tasks import async_task

from .images import thumbnail, optimize
from .utils import WithSentryCapture

log = logging.getLogger(__name__)


def _upload_photo_to_s3(photo_pk):
    """
    Given a photo with a local file on disk, upload it to S3.
    """
    log.info("Processing Photo[%s]", photo_pk)

    from photos.models import Photo

    photo = Photo.objects.get(pk=photo_pk)
    log.info("Fetched Photo[%s] as %s", photo_pk, photo)
    if photo.uploaded_at:
        log.info("Photo[%s] is already uploaded", photo_pk)
        return

    if not photo.local_file:
        msg = "Cannot upload file to S3 - {} is missing local copy".format(photo)
        raise ValueError(msg)

    log.info("Uploading %s original to S3", photo)
    # TODO - stop FS from mangling names
    s3_key = photo.get_original_key(photo.local_file.name)
    s3_storage = photo.file.storage
    fs_storage = photo.local_file.storage
    upload_config = {"ContentType": "image/jpeg"}
    bucket = s3_storage.bucket
    with fs_storage.open(photo.local_file.name, "rb") as f:
        bucket.upload_fileobj(f, s3_key, upload_config)

    photo.file.name = s3_key
    photo.uploaded_at = timezone.now()
    photo.save()

    log.info("Deleting local copy %s from %s", photo.local_file, photo)
    photo.local_file.delete()

    log.info("Finished processing Photo[%s]", photo_pk)
    log.info("Dispatching post-processing for Photo[%s]", photo_pk)
    if not photo.thumbnailed_at:
        async_task(thumbnail_photo, photo.pk)

    if not photo.optimized_at:
        async_task(optimize_photo, photo.pk)

    log.info("Finished dispatching post-processing for Photo[%s]", photo_pk)


def _thumbnail_photo(photo_pk):
    """
    Given a photo that has been uploaded to S3,
    create thumbnails and upload them to S3
    """
    log.info("Thumbnailing a Photo[%s]", photo_pk)
    from photos.models import Photo

    photo = Photo.objects.get(pk=photo_pk)
    log.info("Fetched Photo[%s] as %s", photo_pk, photo)
    if photo.thumbnailed_at:
        log.info("Photo[%s] is already thumbnailed", photo_pk)
    else:
        thumbnail(photo)
        log.info("Finished thumbnailing a Photo[%s]", photo_pk)


def _optimize_photo(photo_pk):
    """
    Given a photo that has been uploaded to S3,
    create an optimized version and upload it to S3
    """
    log.info("Optimizing a Photo[%s]", photo_pk)
    from photos.models import Photo

    photo = Photo.objects.get(pk=photo_pk)
    log.info("Fetched Photo[%s] as %s", photo_pk, photo)
    if photo.optimized_at:
        log.info("Photo[%s] is already optimized", photo_pk)
    else:
        optimize(photo)
        log.info("Finished optimizing Photo[%s]", photo_pk)


upload_photo_to_s3 = WithSentryCapture(_upload_photo_to_s3)
thumbnail_photo = WithSentryCapture(_thumbnail_photo)
optimize_photo = WithSentryCapture(_optimize_photo)
