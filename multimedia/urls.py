from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from multimedia.views import MultimediaViewSet, MultimediaVideoViewSet, \
    MultimediaAudioViewSet, ArticleViewSet, ArticleImageViewSet, CreateArticleWithImageList, \
    CreateMultimediaWithMultimediaList, ListArticleImages, ListMultimediaVideos, ListMultimediaAudios

router = DefaultRouter()
router.register(r"multimedia", MultimediaViewSet, basename="multimedia")
router.register(r"video", MultimediaVideoViewSet, basename="video")
router.register(r"audio", MultimediaAudioViewSet, basename="audio")
router.register(r"article", ArticleViewSet, basename="article")
router.register(r"image", ArticleImageViewSet, basename="image")
urlpatterns = router.urls
urlpatterns += [
    path("article-image", CreateArticleWithImageList.as_view()),
    path("multi-media", CreateMultimediaWithMultimediaList.as_view()),
    path("article/<int:pk>/images", ListArticleImages.as_view()),
    path("multimedia/<int:pk>/audios", ListMultimediaAudios.as_view()),
    path("multimedia/<int:pk>/videos", ListMultimediaVideos.as_view())
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
