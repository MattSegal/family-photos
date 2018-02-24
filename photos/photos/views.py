from django.conf import settings
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import CreateView
from django.utils.text import slugify
from django.db.models import Prefetch
from django.http import JsonResponse

from photos.models import Album, Photo
from photos.forms import PhotoForm

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo_qs = Photo.objects.order_by('-taken_at').only('file')
        prefetch = Prefetch('photo_set', queryset=photo_qs)
        albums = Album.objects.prefetch_related(prefetch).all()
        context.update({
            'thumb_height': settings.THUMBNAIL_HEIGHT,
            'thumb_width': settings.THUMBNAIL_WIDTH,
            'albums': albums,
        })
        return context


class AlbumView(DetailView):
    model = Album
    template_name = 'album.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album_photos = (
            Photo.objects
            .filter(album=self.object)
            .order_by('-taken_at')
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
            title = request.FILES['file']._name
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
