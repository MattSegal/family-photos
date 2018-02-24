import logging
from django.db import models

from photos.images import get_s3_key, thumbnail

logger = logging.getLogger(__name__)


class Album(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnailed_at = models.DateTimeField(null=True, blank=True)
    taken_at = models.DateTimeField(null=True, blank=True)
    album = models.ForeignKey(Album, null=True, on_delete=models.SET_NULL)
    file = models.ImageField(upload_to=get_s3_key)

    def save(self, *args, **kwargs):
        # When creating the photo for the first time.
        # ensure that we don't create duplicate database entries
        if not self.pk:
            file_name = get_s3_key(self, self.file.name)
            if Photo.objects.filter(file=file_name).exists():
                msg = '{} is already uploaded as {}'.format(self, file_name)
                logger.info(msg)
                raise Photo.AlreadyUploaded(msg)

        super().save(*args, **kwargs)
        if not self.thumbnailed_at:
            thumbnail(self)

    def get_original_key(self, filename):
        return 'original/{}'.format(filename)

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
