from django.urls import path
from rest_framework.routers import DefaultRouter

from article.views.actions import (ArticleApprovalView, ArticlePinView,
                                   ArticleStatusForMe, BookmarkView, LoveView)
from article.views.article import (ArticleViewSet, ArticleWithImageListView,
                                   CompleteWriting, StartWritingView)
from article.views.comment import CommentViewSet
from article.views.list import ListBookmarkedView, ListLovedView
from article.views.media import (ArticleImageUrlViewSet, ArticleImageViewSet,
                                 CoverImageViewSet)

router = DefaultRouter()
router.register(r"article", ArticleViewSet, basename="article")
router.register(r"article-image", ArticleImageViewSet, basename="article-image")
router.register(r"article-cover", CoverImageViewSet, basename="article-image")
router.register(
    r"article-image-url", ArticleImageUrlViewSet, basename="article-image-url"
)
router.register(r"article-comment", CommentViewSet, basename="article-comment")

urlpatterns = router.urls

urlpatterns += [
    path("start-writing", StartWritingView.as_view()),
    path("article/<int:pk>/complete-writing", CompleteWriting.as_view()),
    path("create-article", ArticleWithImageListView.as_view()),
    path("article/<int:pk>/status", ArticleStatusForMe.as_view()),
    path("article/<int:pk>/approve", ArticleApprovalView.as_view()),
    path("article/<int:pk>/pin", ArticlePinView.as_view()),
    path("article/<int:pk>/love", LoveView.as_view()),
    path(
        "article/<int:pk>/bookmark",
        BookmarkView.as_view(),
    ),
    path("loved-article", ListLovedView.as_view()),
    path("bookmarked-article", ListBookmarkedView.as_view()),
]
