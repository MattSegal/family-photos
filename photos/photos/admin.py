from django.contrib import admin

from photos.models import Photo, Album

admin.site.register(Album)
admin.site.register(Photo)
