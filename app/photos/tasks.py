import os
import zipfile
import shutil

from celery import shared_task, chord
from celery.utils.log import get_task_logger
from django.utils import timezone

from photos.images import thumbnail, optimize

log = get_task_logger(__name__)


@shared_task
def upload_photo_to_s3(photo_pk):
    """
    Given a photo with a local file on disk, upload it to S3.
    """
    log.info('Processing Photo[%s]', photo_pk)

    from photos.models import Photo
    photo = Photo.objects.get(pk=photo_pk)
    log.info('Fetched Photo[%s] as %s', photo_pk, photo)
    if photo.uploaded_at:
        log.info('Photo[%s] is already uploaded', photo_pk)
        return

    if not photo.local_file:
        msg = 'Cannot upload file to S3 - {} is missing local copy'.format(photo)
        raise ValueError(msg)

    log.info('Uploading %s original to S3', photo)
    # TODO - stop FS from mangling names
    s3_key = photo.get_original_key(photo.local_file.name)
    s3_storage = photo.file.storage
    fs_storage = photo.local_file.storage
    upload_config = {'ContentType': 'image/jpeg'}
    bucket = s3_storage.bucket
    with fs_storage.open(photo.local_file.name, 'rb') as f:
        bucket.upload_fileobj(f, s3_key, upload_config)

    photo.file.name = s3_key
    photo.uploaded_at = timezone.now()
    photo.save()

    log.info('Deleting local copy %s from %s', photo.local_file, photo)
    photo.local_file.delete()

    log.info('Finished processing Photo[%s]', photo_pk)
    log.info('Dispatching post-processing for Photo[%s]', photo_pk)
    if not photo.thumbnailed_at:
        thumbnail_photo.delay(photo.pk)

    if not photo.optimized_at:
        optimize_photo.delay(photo.pk)

    log.info('Finished dispatching post-processing for Photo[%s]', photo_pk)


@shared_task
def thumbnail_photo(photo_pk):
    """
    Given a photo that has been uploaded to S3,
    create thumbnails and upload them to S3
    """
    log.info('Thumbnailing a Photo[%s]', photo_pk)
    from photos.models import Photo
    photo = Photo.objects.get(pk=photo_pk)
    log.info('Fetched Photo[%s] as %s', photo_pk, photo)
    if photo.thumbnailed_at:
        log.info('Photo[%s] is already thumbnailed', photo_pk)
    else:
        thumbnail(photo)
        log.info('Finished thumbnailing a Photo[%s]', photo_pk)


@shared_task
def optimize_photo(photo_pk):
    """
    Given a photo that has been uploaded to S3,
    create an optimized version and upload it to S3
    """
    log.info('Optimizing a Photo[%s]', photo_pk)
    from photos.models import Photo
    photo = Photo.objects.get(pk=photo_pk)
    log.info('Fetched Photo[%s] as %s', photo_pk, photo)
    if photo.optimized_at:
        log.info('Photo[%s] is already optimized', photo_pk)
    else:
        optimize(photo)
        log.info('Finished optimizing Photo[%s]', photo_pk)


@shared_task
def prepare_album_download(album_pk):
    """
    Prepare a ZIP file of all photos in an album,
    which a user can download from S3.
    """
    from photos.models import Album, AlbumDownload
    album = Album.objects.get(pk=album_pk)
    AlbumDownload.objects.get_or_create(album=album)
    download_dir = f'/photos/download/{album.slug}/'
    os.makedirs(download_dir, exist_ok=True)
    download_tasks = []
    for photo in album.photo_set.all():
        download_tasks.append(prepare_photo_download.si(photo.pk, download_dir))

    # Download all photos, then package album download
    next_tasks = chord(download_tasks, package_album_download.si(album_pk, download_dir))
    next_tasks()


@shared_task
def package_album_download(album_pk, download_dir):
    """
    Packages album files into a ZIP and uploads it to S3
    """
    from photos.models import Album, AlbumDownload
    album = Album.objects.get(pk=album_pk)
    download = AlbumDownload.objects.get(album=album)
    file_paths = [
        f'{download_dir}{fn}' for fn in os.listdir(download_dir)
        if not fn.endswith('.zip')
    ]
    log.info('ZIPPING  %s', file_paths)

    zip_path = f'{download_dir}{album.slug}.zip'
    log.info('Creating ZIP file  %s', zip_path)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for file_path in file_paths:
            zf.write(file_path)

    log.info('Finished creating ZIP file  %s', zip_path)

    storage = download.file.storage
    bucket = storage.bucket
    upload_config = {
        'ContentType': 'application/x-zip-compressed',
        'ACL': 'public-read'
    }
    key = f'zip/{album.slug}.zip'
    log.info('Uploading %s', key)
    with open(zip_path, 'rb') as zf:
        bucket.upload_fileobj(zf, key, upload_config)

    log.info('Finished uploading %s', key)
    log.info('Cleanining up %s', download_dir)
    shutil.rmtree(download_dir)
    log.info('Finished cleaning up %s', download_dir)

    log.info('Updating AlbumDownload[%s]', download.pk)
    download.file.name = key
    download.uploaded_at = timezone.now()
    download.save()
    log.info('Finished updating AlbumDownload[%s]', download.pk)


@shared_task(bind=True)
def prepare_photo_download(self, photo_pk, download_dir):
    """
    Fetch a photo from S3 to the local filesystem, so that it can be zipped up.
    """
    from photos.models import Photo
    photo = Photo.objects.get(pk=photo_pk)
    storage = photo.file.storage
    source_file = photo.file.name.replace('original', 'optimized')
    filename = source_file.split('/')[-1]
    target_file = f'{download_dir}{filename}'
    if os.path.exists(target_file):
        log.info(f'Did not download Photo[{photo_pk}] - already exists')
    else:
        log.info(f'Downloading Photo[{photo_pk}] for ZIP file.')
        try:
            with storage.open(source_file, 'rb') as s3_file:
                with open(target_file, 'wb') as local_file:
                    local_file.write(s3_file.read())
        except Exception as e:
            log.exception(f'Failed to download Photo[{photo_pk}]')
            raise self.retry(exc=e, countdown=20, max_retries=2)
