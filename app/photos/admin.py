from django.contrib import admin
from django.contrib.messages import constants as messages
from django.utils.html import format_html

from photos.models import Photo, Album, AlbumDownload
from photos.tasks import thumbnail_photo, prepare_album_download, optimize_photo, upload_photo_to_s3



admin.site.register(Album)

@admin.register(Photo)
class Photo(admin.ModelAdmin):
    list_display = (
        'title',
        'created_at',
        'uploaded_at',
        'thumbnailed_at',
        'optimized_at',
        'taken_at',
        'image_tag_list',

    )
    actions = ['thumbnail', 'optimize', 'upload_local']

    readonly_fields = (
        'image_tag',
        'created_at',
        'local_file',
    )

    def thumbnail(self, request, queryset):
        for photo in queryset:
            thumbnail_photo.delay(photo.pk)

        self.message_user(request, 'Thumbnailing tasks dispatched.', level=messages.INFO)

    thumbnail.short_description = 'Thumbnail photos'

    def optimize(self, request, queryset):
        for photo in queryset:
            optimize_photo.delay(photo.pk)

        self.message_user(request, 'Optimization tasks dispatched.', level=messages.INFO)

    optimize.short_description = 'Optimize photos'

    def upload_local(self, request, queryset):
        for photo in queryset:
            upload_photo_to_s3.delay(photo.pk)

        self.message_user(request, 'Upload tasks dispatched.', level=messages.INFO)

    upload_local.short_description = 'Upload local photos'

    def image_tag_list(self, photo):
        url = photo.file.url.replace('original', 'thumbnail') if photo.file else '#'
        return format_html('<img height="60px" src="{}" />', url)

    image_tag_list.short_description = 'Preview'


    def image_tag(self, photo):
        url = photo.file.url.replace('original', 'thumbnail') if photo.file else '#'
        return format_html('<img width="300px" src="{}" />', url)

    image_tag.short_description = 'Preview'


@admin.register(AlbumDownload)
class AlbumDownload(admin.ModelAdmin):

    actions = ['prepare']

    def prepare(self, request, queryset):
        for download in queryset:
            prepare_album_download.delay(download.album.pk)

        self.message_user(request, 'Download tasks dispatched.', level=messages.INFO)
