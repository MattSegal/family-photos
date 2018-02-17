from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.utils.text import slugify

from photos.models import Album

class LandingView(TemplateView):
    template_name = 'landing.html'


class CreateAlbumView(CreateView):
    template_name = 'album_create.html'
    success_url = '/album/created/'
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
