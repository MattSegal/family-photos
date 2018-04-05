from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from photos import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('album/create/success/', views.CreateAlbumSuccessView.as_view(), name='album-created'),
    path('album/create/', views.CreateAlbumView.as_view(), name='album-create'),
    path('album/<slug:slug>/', views.AlbumView.as_view(), name='album-detail'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('review/', views.ReviewView.as_view(), name='review'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
