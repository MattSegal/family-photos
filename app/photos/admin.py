from django.contrib import admin
from django.contrib.messages import constants as messages

from photos.models import Photo, Album
from photos.tasks import thumbnail_photo


admin.site.register(Album)

@admin.register(Photo)
class Photo(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'uploaded_at', 'thumbnailed_at', 'taken_at')
    actions = ['thumbnail']

    readonly_fields = (
        'created_at',
        'local_file',
    )

    def thumbnail(self, request, queryset):
        for photo in queryset:
            thumbnail_photo.delay(photo.pk)

        self.message_user(request, 'Thumbnailing tasks dispatched.', level=messages.INFO)

    thumbnail.short_description = 'Thumbnail photos'
