from django.urls import path
from rest_framework.routers import DefaultRouter

from multimedia.views.action import (ApprovalView, BookmarkView, LoveView,
                                     MultimediaStatusForMe, PinView)
from multimedia.views.comment import CommentViewSet
from multimedia.views.list import ListBookmarkedView, ListLovedView
from multimedia.views.media import (SoundViewSet,
                                    ImageViewSet,
                                    VideoUrlViewSet,
                                    VideoViewSet)
from multimedia.views.multimedia import (MultimediaViewSet,
                                         MultimediaWithMediaListView)

router = DefaultRouter()
router.register(r"multimedia", MultimediaViewSet, basename="multimedia")
router.register(
    r"multimedia-image", ImageViewSet, basename="multimedia-image"
)
router.register(
    r"multimedia-sound", SoundViewSet, basename="multimedia-sound"
)
router.register(
    r"multimedia-video", VideoViewSet, basename="multimedia-video"
)
router.register(
    r"multimedia-video-url", VideoUrlViewSet, basename="multimedia-video-url"
)
router.register(r"multimedia-comment", CommentViewSet, basename="multimedia-comment")
urlpatterns = router.urls


urlpatterns += [
    path("create-multimedia", MultimediaWithMediaListView.as_view()),
    path("multimedia/<int:pk>/approve", ApprovalView.as_view()),
    path("multimedia/<int:pk>/pin", PinView.as_view()),
    path(
        "multimedia/<int:pk>/love",
        LoveView.as_view(),
    ),
    path(
        "multimedia/<int:pk>/bookmark",
        BookmarkView.as_view(),
    ),
    path("multimedia/<int:pk>/status", MultimediaStatusForMe.as_view()),
    path("loved-media", ListLovedView.as_view()),
    path("bookmarked-media", ListBookmarkedView.as_view()),
]
