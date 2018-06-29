from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from photos import views

router = routers.DefaultRouter()
router.register('album', views.AlbumViewSet)

urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('album/<slug:slug>/', views.AlbumView.as_view(), name='album-detail'),
    path('api/', include(router.urls)),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
