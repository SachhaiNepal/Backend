from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from multimedia.views import MultimediaViewSet, MultimediaVideoViewSet, \
    MultimediaAudioViewSet, ArticleViewSet, ArticleImageViewSet

router = DefaultRouter()
router.register(r"multimedia", MultimediaViewSet, basename="multimedia")
router.register(r"video", MultimediaVideoViewSet, basename="video")
router.register(r"audio", MultimediaAudioViewSet, basename="audio")
router.register(r"article", ArticleViewSet, basename="article")
router.register(r"image", ArticleImageViewSet, basename="image")
urlpatterns = router.urls
urlpatterns += [
    #
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
