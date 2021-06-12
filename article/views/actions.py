from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from article.serializers.action import (BookmarkThinSerializer,
                                        LoveThinSerializer)
from article.serializers.article import ArticleCreateSerializer
from article.sub_models.action import Bookmark, Love
from article.sub_models.article import Article


class ArticleApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        article = get_object_or_404(Article, pk=pk)
        if not article.is_approved:
            article.is_approved = True
            article.approved_by = request.user
            article.approved_at = timezone.now()
            article.save()
            return Response(
                ArticleCreateSerializer(article).data, status=status.HTTP_201_CREATED
            )
        return Response(
            ArticleCreateSerializer(article).data, status=status.HTTP_200_OK
        )

    @staticmethod
    def delete(request, pk):
        article = get_object_or_404(Article, pk=pk)
        if article.is_approved:
            article.is_approved = False
            article.approved_by = None
            article.approved_at = None
            article.save()
            return Response(
                ArticleCreateSerializer(article).data, status=status.HTTP_201_CREATED
            )
        return Response(
            ArticleCreateSerializer(article).data, status=status.HTTP_200_OK
        )


class ArticleStatusForMe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        article = get_object_or_404(Article, pk=pk)
        love, created = Love.objects.get_or_create(article=article, lover=request.user)
        bookmark, created = Bookmark.objects.get_or_create(
            article=article, marker=request.user
        )
        loves = Love.objects.filter(article=article, is_loved=True)
        bookmarks = Bookmark.objects.filter(article=article, is_bookmarked=True)
        return Response(
            {
                "loved": love.is_loved,
                "bookmarked": bookmark.is_bookmarked,
                "pinned": article.is_pinned,
                "love_count": loves.count(),
                "bookmark_count": bookmarks.count(),
            },
            status=status.HTTP_200_OK,
        )


class ArticlePinView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.is_pinned = True
        article.pinner = request.user
        article.save()
        return Response(
            ArticleCreateSerializer(article).data, status=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def delete(request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.is_pinned = False
        article.pinner = None
        article.save()
        return Response(
            ArticleCreateSerializer(article).data, status=status.HTTP_204_NO_CONTENT
        )


class BookmarkView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        article = get_object_or_404(Article, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(
            article=article, marker=request.user
        )
        bookmark.is_bookmarked = True
        bookmark.save()
        return Response(
            BookmarkThinSerializer(bookmark).data, status=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def delete(request, pk):
        article = get_object_or_404(Article, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(
            article=article, marker=request.user
        )
        bookmark.is_bookmarked = False
        bookmark.save()
        return Response(
            BookmarkThinSerializer(bookmark).data, status=status.HTTP_204_NO_CONTENT
        )


class LoveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        article = get_object_or_404(Article, pk=pk)
        love, created = Love.objects.get_or_create(article=article, lover=request.user)
        love.is_loved = True
        love.save()
        return Response(
            LoveThinSerializer(love).data, status=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def delete(request, pk):
        article = get_object_or_404(Article, pk=pk)
        love, created = Love.objects.get_or_create(article=article, lover=request.user)
        love.is_loved = False
        love.save()
        return Response(
            LoveThinSerializer(love).data, status=status.HTTP_204_NO_CONTENT
        )
