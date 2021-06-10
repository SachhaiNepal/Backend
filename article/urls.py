from django.urls import path
from rest_framework.routers import DefaultRouter

from article.views.actions import (ArticleApprovalView, ArticlePinView,
                                   ArticleStatusForMe, BookmarkView, LoveView)
from article.views.article import ArticleViewSet, ArticleWithImageListView
from article.views.comment import CommentViewSet
from article.views.list import ListBookmarkedView, ListLovedView
from article.views.media import ArticleImageViewSet

router = DefaultRouter()
router.register(r"article", ArticleViewSet, basename="article")
router.register(r"article-image", ArticleImageViewSet, basename="article-image")
router.register(r"article-comment", CommentViewSet, basename="article-comment")

urlpatterns = router.urls

urlpatterns += [
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
