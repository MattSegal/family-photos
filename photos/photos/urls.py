from django.contrib import admin
from django.urls import path

from photos import views

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('album/created/', views.CreateAlbumSuccessView.as_view(), name='album-created'),
    path('album/', views.CreateAlbumView.as_view(), name='album-create'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('admin/', admin.site.urls),
]
