import json

from django.conf import settings
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView
from django.utils.text import slugify
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Album, Photo
from .forms import PhotoForm
from .tasks import upload_photo_to_s3, thumbnail_photo
from .permissions import IsOwnerOrReadOnly
from .serializers import AlbumListSerializer, AlbumSerializer

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        albums = Album.objects.all()

        context['bootstrap_data'] = json.dumps({
            'thumb_height': settings.THUMBNAIL_HEIGHT,
            'thumb_width': settings.THUMBNAIL_WIDTH,
            'albums': AlbumListSerializer(albums, many=True).data
        })
        return context


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


class AlbumView(DetailView):
    model = Album
    template_name = 'album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_photos = (
            Photo.objects
            .filter(album=self.object)
            .exclude(file='')
            .order_by('taken_at')
            .all()
            .only('file')
        )

        context.update({
            'thumb_height': settings.THUMBNAIL_HEIGHT,
            'thumb_width': settings.THUMBNAIL_WIDTH,
            'photos': album_photos,
        })
        return context


class CreateAlbumView(CreateView):
    template_name = 'album_create.html'
    success_url = '/album/create/success/'
    model = Album
    fields = ['name']

    def form_valid(self, form):
         form.instance.slug = slugify(form.instance.name)
         return super(CreateAlbumView, self).form_valid(form)


class CreateAlbumSuccessView(TemplateView):
    template_name = 'album_success.html'


class UploadView(TemplateView):
    template_name = 'upload.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['albums'] = Album.objects.all()
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
        else:
            data = {'is_valid': False, 'errors': form.errors}
        return JsonResponse(data)


class ReviewView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = '/admin/login/'
    redirect_field_name = 'next'
    template_name = 'review.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        not_uploaded_photos = Photo.objects.filter(uploaded_at__isnull=True)
        not_thumbnailed_photos = Photo.objects.filter(thumbnailed_at__isnull=True).difference(not_uploaded_photos)
        context['not_uploaded_photos'] = not_uploaded_photos
        context['not_thumbnailed_photos'] = not_thumbnailed_photos
        return context

    def post(self, request):
        not_uploaded_photos = Photo.objects.filter(uploaded_at__isnull=True)
        not_thumbnailed_photos = Photo.objects.filter(thumbnailed_at__isnull=True).difference(not_uploaded_photos)
        for p in not_thumbnailed_photos:
            thumbnail_photo.delay(p.pk)
        for p in not_uploaded_photos:
            upload_photo_to_s3.delay(p.pk)

        return HttpResponseRedirect('/review/')
