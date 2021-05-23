from django.urls import path
from rest_framework.routers import DefaultRouter

from multimedia.views.article import (ArticleViewSet,
                                      CreateArticleWithImageList,
                                      ToggleArticleApprovalView)
from multimedia.views.article_image import (ArticleImageDetailView,
                                            ListArticleImages)
from multimedia.views.bookmark import (
    CreateOrToggleBookmarkStatusOfArticle,
    CreateOrToggleBookmarkStatusOfMultimedia)
from multimedia.views.comment import (ListArticleComments,
                                      ListMultimediaComments, PostComment)
from multimedia.views.love import (CreateOrToggleLoveStatusOfArticle,
                                   CreateOrToggleLoveStatusOfMultimedia)
from multimedia.views.multimedia import (CreateMultimediaWithMultimediaList,
                                         MultimediaViewSet,
                                         ToggleMultimediaApprovalView)
from multimedia.views.multimedia_media import (ListMultimediaAudios,
                                               ListMultimediaImages,
                                               ListMultimediaVideos,
                                               ListMultimediaVideoUrls)
from multimedia.views.multimedia_media_detail import (
    MultimediaAudioDetailView, MultimediaImageDetailView,
    MultimediaVideoDetailView)
from multimedia.views.pin_post import (CreateOrTogglePinStatusOfArticle,
                                       CreateOrTogglePinStatusOfMultimedia)
from multimedia.views.post_list import (ListBookmarkedMediaView,
                                        ListLovedMediaView,
                                        ListPinnedMediaView)
from multimedia.views.post_status import ArticleStatus, MultimediaStatus

router = DefaultRouter()
router.register(r"multimedia", MultimediaViewSet, basename="multimedia")
router.register(r"article", ArticleViewSet, basename="article")
urlpatterns = router.urls
urlpatterns += [
    path("create-article", CreateArticleWithImageList.as_view()),
    path("create-multimedia", CreateMultimediaWithMultimediaList.as_view()),
    path("article/<int:pk>/image", ListArticleImages.as_view()),
    path("multimedia/<int:pk>/video", ListMultimediaVideos.as_view()),
    path("multimedia/<int:pk>/audio", ListMultimediaAudios.as_view()),
    path("multimedia/<int:pk>/image", ListMultimediaImages.as_view()),
    path("multimedia/<int:pk>/video-url", ListMultimediaVideoUrls.as_view()),
    path("article-image/<int:pk>", ArticleImageDetailView.as_view()),
    path("multimedia-image/<int:pk>", MultimediaImageDetailView.as_view()),
    path("multimedia-audio/<int:pk>", MultimediaAudioDetailView.as_view()),
    path("multimedia-video/<int:pk>", MultimediaVideoDetailView.as_view()),
    path("multimedia/<int:pk>/toggle-approval", ToggleMultimediaApprovalView.as_view()),
    path("article/<int:pk>/toggle-approval", ToggleArticleApprovalView.as_view()),
    path("article/<int:pk>/toggle-love", CreateOrToggleLoveStatusOfArticle.as_view()),
    path(
        "article/<int:pk>/toggle-bookmark",
        CreateOrToggleBookmarkStatusOfArticle.as_view(),
    ),
    path(
        "article/<int:pk>/toggle-pin-status",
        CreateOrTogglePinStatusOfArticle.as_view(),
    ),
    path("article-status/<int:pk>", ArticleStatus.as_view()),
    path(
        "multimedia/<int:pk>/toggle-love",
        CreateOrToggleLoveStatusOfMultimedia.as_view(),
    ),
    path(
        "multimedia/<int:pk>/toggle-bookmark",
        CreateOrToggleBookmarkStatusOfMultimedia.as_view(),
    ),
    path(
        "multimedia/<int:pk>/toggle-pin-status",
        CreateOrTogglePinStatusOfMultimedia.as_view(),
    ),
    path("multimedia-status/<int:pk>", MultimediaStatus.as_view()),
    path("multimedia/<int:pk>/comment", ListMultimediaComments.as_view()),
    path("article/<int:pk>/comment", ListArticleComments.as_view()),
    path("comment", PostComment.as_view()),
    path("loved-media", ListLovedMediaView.as_view()),
    path("bookmarked-media", ListBookmarkedMediaView.as_view()),
    path("pinned-media", ListPinnedMediaView.as_view()),
]
