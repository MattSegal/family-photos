import logging
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.db.models import Q

from photos.images import get_s3_key, get_local_filename, thumbnail
from photos.tasks import upload_photo_to_s3

logger = logging.getLogger(__name__)
file_storage = FileSystemStorage(location=settings.LOCAL_MEDIA_ROOT)

class Album(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField()

    def thumbnailed_photos(self):
        return (
            self.photo_set
            .exclude(
                Q(file='') |
                Q(file__isnull=True) |
                Q(thumbnailed_at__isnull=True)
            )
            .order_by('-taken_at')
        )

    def __str__(self):
        return self.name


def get_download_filename(f):
    return f'downloads/{filename}'


class AlbumDownload(models.Model):
    # Time when user created a download request
    created_at = models.DateTimeField(auto_now_add=True)
    # Time when the ZIP file was uploaded to S3
    uploaded_at = models.DateTimeField(null=True, blank=True)
    album = models.ForeignKey(Album, null=True, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=get_download_filename,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.album.name


class Photo(models.Model):
    title = models.CharField(max_length=255)
    # When the Photo was created
    created_at = models.DateTimeField(auto_now_add=True)
    # When the image was uploaded to S3
    uploaded_at = models.DateTimeField(null=True, blank=True)
    # When the image was thumbnailed
    thumbnailed_at = models.DateTimeField(null=True, blank=True)
    # When the image was optimized
    optimized_at = models.DateTimeField(null=True, blank=True)
    # When the image was taken
    taken_at = models.DateTimeField(null=True, blank=True)
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL)

    # File uploaded to S3
    file = models.ImageField(
        upload_to=get_s3_key,
        null=True,
        blank=True
    )
    # Local file on disk
    local_file = models.ImageField(
        upload_to=get_local_filename,
        storage=file_storage,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        # When creating the photo for the first time.
        # ensure that we don't create duplicate database entries
        if not self.pk:
            img_bytes = self.local_file._file.file.read()
            self.local_file._file.file.seek(0)
            local_filename = get_local_filename(self, self.local_file.name)
            s3_key = self.get_original_key(local_filename)

            exists_locally = Photo.objects.filter(local_file=local_filename).exists()
            exists_s3 = Photo.objects.filter(file=s3_key).exists()
            if exists_locally or exists_s3:
                msg = '{} is already uploaded as {}'.format(self, local_filename)
                if exists_locally:
                    msg += '. File is present locally.'
                if exists_s3:
                    msg += '. File is present on S3.'
                logger.info(msg)
                raise Photo.AlreadyUploaded(msg)
            else:
                logger.info('Saving new photo with local filename %s', local_filename)

        super().save(*args, **kwargs)

        if not self.uploaded_at:
            upload_photo_to_s3.delay(self.pk)

    def get_original_key(self, filename):
        return 'original/{}'.format(filename)

    def get_optimized_key(self):
        return self.file.name.replace('original/', 'optimized/')

    def get_thumb_key(self):
        return self.file.name.replace('original/', 'thumbnail/')

    def get_display_key(self):
        return self.file.name.replace('original/', 'display/')

    def get_thumb_url(self):
        return self.file.url.replace('original/', 'thumbnail/')

    def __str__(self):
        return self.title

    class AlreadyUploaded(Exception):
        # Throw when Photo file is already uploaded
        pass
