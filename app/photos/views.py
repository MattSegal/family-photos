import json

from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.utils.text import slugify
from django.db.models import Max
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Album, Photo
from .forms import PhotoForm
from .tasks import upload_photo_to_s3, thumbnail_photo
from .permissions import IsOwnerOrReadOnly
from .serializers import AlbumListSerializer, AlbumSerializer


class AppView(TemplateView):
    template_name = 'app.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        albums = (
            Album.objects.all().prefetch_related('photo_set')
            .annotate(latest_photo=Max('photo__thumbnailed_at'))
            .order_by('-latest_photo')
        )

        bootstrap_data = {
            'thumb_height': settings.THUMBNAIL_HEIGHT,
            'thumb_width': settings.THUMBNAIL_WIDTH,
            'albums': AlbumListSerializer(albums, many=True).data,
            'title': 'Memories Ninja'
        }
        bootstrap_data.update(kwargs.get('bootstrap_data', {}))
        context['bootstrap_data'] = json.dumps(bootstrap_data)
        context['title'] = 'Memories Ninja'
        context['albums'] = albums
        return context


class LandingView(AppView):
    pass


class AlbumView(AppView):

    def get_context_data(self, **kwargs):
        slug = kwargs.get('slug')
        try:
            album = Album.objects.get(slug=slug)
            title = album.name
        except Album.DoesNotExist:
            title = 'Not Found'

        kwargs['bootstrap_data'] = {
            'title': title
        }

        context = super().get_context_data(**kwargs)
        context['title'] = title
        return context


class UploadView(AppView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Uploads'
        return context

    def post(self, request):
        try:
            title = request.FILES['local_file']._name
        except (IndexError, KeyError, AttributeError):
            title = None

        post_data = request.POST.copy()
        post_data['title'] = title

        form = PhotoForm(post_data, request.FILES)
        if form.is_valid():
            try:
                photo = form.save()
            except Photo.AlreadyUploaded:
                pass
            data = {'is_valid': True}
            status = 200
        else:
            data = {'is_valid': False, 'errors': form.errors}
            status = 400
        return JsonResponse(data, status=status)


class AlbumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def list(self, request, *args, **kwargs):
        """
        Use AlbumListSerializer if we request a list view
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AlbumListSerializer(queryset, many=True)
        return Response(serializer.data)
