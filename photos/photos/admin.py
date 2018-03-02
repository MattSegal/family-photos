from django.contrib import admin

from photos.models import Photo, Album

admin.site.register(Album)

@admin.register(Photo)
class Photo(admin.ModelAdmin):
    readonly_fields = (
        'created_at',
        'local_file',
    )
