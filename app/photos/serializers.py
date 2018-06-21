from rest_framework import serializers

from .models import Album, Photo


class PhotoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    taken_at = serializers.DateTimeField(read_only=True)
    thumb_url = serializers.SerializerMethodField()
    display_url = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ('id', 'thumb_url', 'display_url', 'taken_at')

    def get_thumb_url(self, obj):
        try:
            return obj.file.url.replace('/original/', '/thumbnail/')
        except AttributeError:
            return ''

    def get_display_url(self, obj):
        try:
            return obj.file.url.replace('/original/', '/display/')
        except AttributeError:
            return ''


class AlbumListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ('id', 'name', 'slug', 'photos')

    def get_photos(self, obj):
        # Is this an inefficient query? Can we do better?
        return PhotoSerializer(obj.thumbnailed_photos()[:4], many=True).data


class AlbumSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ('id', 'name', 'slug', 'photos')
        list_serializer_class = AlbumListSerializer

    def get_photos(self, obj):
        # Is this an inefficient query? Can we do better?
        return PhotoSerializer(obj.thumbnailed_photos(), many=True).data

