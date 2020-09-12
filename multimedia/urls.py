from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from multimedia.views.getters import *
from multimedia.views.list_uploader import *
from multimedia.views import views

router = DefaultRouter()
router.register(r"multimedia", views.MultimediaViewSet, basename="multimedia")
# router.register(r"multimedia/video", views.MultimediaVideoViewSet, basename="multimedia-video")
# router.register(r"multimedia/audio", views.MultimediaAudioViewSet, basename="multimedia-audio")
# router.register(r"multimedia/image", views.MultimediaImageViewSet, basename="multimedia-image")
router.register(r"article", views.ArticleViewSet, basename="article")
# router.register(r"article/image", views.ArticleImageViewSet, basename="article-image")
urlpatterns = router.urls
urlpatterns += [
    path("create-article", CreateArticleWithImageList.as_view()),
    path("create-multimedia", CreateMultimediaWithMultimediaList.as_view()),
    path("article/<int:pk>/image", ListArticleImages.as_view()),
    path("multimedia/<int:pk>/video", ListMultimediaVideos.as_view()),
    path("multimedia/<int:pk>/audio", ListMultimediaAudios.as_view()),
    path("multimedia/<int:pk>/image", ListMultimediaImages.as_view())
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
