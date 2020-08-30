from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from multimedia.views.getters import ListArticleImages, ListMultimediaAudios, ListMultimediaVideos
from multimedia.views.list_uploader import CreateArticleWithImageList, CreateMultimediaWithMultimediaList
from multimedia.views import views

router = DefaultRouter()
router.register(r"multimedia", views.MultimediaViewSet, basename="multimedia")
router.register(r"video", views.MultimediaVideoViewSet, basename="video")
router.register(r"audio", views.MultimediaAudioViewSet, basename="audio")
router.register(r"article", views.ArticleViewSet, basename="article")
router.register(r"image", views.ArticleImageViewSet, basename="image")
urlpatterns = router.urls
urlpatterns += [
    path("article-image", CreateArticleWithImageList.as_view()),
    path("multi-media", CreateMultimediaWithMultimediaList.as_view()),
    path("article/<int:pk>/images", ListArticleImages.as_view()),
    path("multimedia/<int:pk>/audios", ListMultimediaAudios.as_view()),
    path("multimedia/<int:pk>/videos", ListMultimediaVideos.as_view())
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
