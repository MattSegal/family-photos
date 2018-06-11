from django.contrib import admin

from photos.models import Photo, Album

admin.site.register(Album)

@admin.register(Photo)
class Photo(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'uploaded_at', 'taken_at')

    readonly_fields = (
        'created_at',
        'local_file',
    )
