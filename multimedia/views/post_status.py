from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import (
    Article, BookmarkMedia, Love,
    Multimedia, PinMedia
)


class ArticleStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        article = get_object_or_404(Article, pk=pk)
        love, created = Love.objects.get_or_create(article=article, lover=request.user)
        bookmark, created = BookmarkMedia.objects.get_or_create(
            article=article, marker=request.user
        )
        pin, created = PinMedia.objects.get_or_create(
            article=article, pinner=request.user
        )
        love_count = Love.objects.filter(article=article, is_loved=True).count()

        bookmark_count = BookmarkMedia.objects.filter(
            article=article, is_bookmarked=True
        ).count()
        pin_count = PinMedia.objects.filter(
            article=article, is_pinned=True
        ).count()
        return Response(
            {
                "loved"         : love.is_loved,
                "bookmarked"    : bookmark.is_bookmarked,
                "pinned"        : pin.is_pinned,
                "love_count"    : love_count,
                "bookmark_count": bookmark_count,
                "pin_count"     : pin_count,
            },
            status=status.HTTP_200_OK,
        )


class MultimediaStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        love, created = Love.objects.get_or_create(
            multimedia=multimedia, lover=request.user
        )
        bookmark, created = BookmarkMedia.objects.get_or_create(
            multimedia=multimedia, marker=request.user
        )
        pin, created = PinMedia.objects.get_or_create(
            multimedia=multimedia, pinner=request.user
        )
        love_count = Love.objects.filter(multimedia=multimedia, is_loved=True).count()
        bookmark_count = BookmarkMedia.objects.filter(
            multimedia=multimedia, is_bookmarked=True
        ).count()
        pin_count = PinMedia.objects.filter(
            multimedia=multimedia, is_pinned=True
        ).count()
        return Response(
            {
                "loved"         : love.is_loved,
                "bookmarked"    : bookmark.is_bookmarked,
                "pinned"        : pin.is_pinned,
                "love_count"    : love_count,
                "bookmark_count": bookmark_count,
                "pin_count"     : pin_count,
            },
            status=status.HTTP_200_OK,
        )
