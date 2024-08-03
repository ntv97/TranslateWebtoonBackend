from .views import ImageViewSet

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('image/translate', ImageViewSet.as_view({
        'post': 'retrieve'
    })),
    path('image/resize', ImageViewSet.as_view({
        'post': 'resize'
    }))
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
