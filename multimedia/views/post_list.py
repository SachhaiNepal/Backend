from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import BookmarkMedia, Love, PinMedia
from multimedia.serializers.article_actions import (BookmarkMediaSerializer,
                                                    LoveSerializer,
                                                    PinMediaSerializer)


def remove_duplicates(media_array):
    id_array = []
    unique_set = []
    for media in media_array:
        if media.pk in id_array:
            continue
        else:
            id_array.append(media.pk)
            unique_set.append(media)
    return unique_set


class ListLovedMediaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        loved_articles = Love.objects.filter(multimedia=None, is_loved=True)
        loved_multimedias = Love.objects.filter(article=None, is_loved=True)
        loved_articles_unique_set = remove_duplicates(loved_articles)
        loved_multimedias_unique_set = remove_duplicates(loved_multimedias)
        article_serializer = LoveSerializer(loved_articles_unique_set, many=True)
        multimedia_serializer = LoveSerializer(loved_multimedias_unique_set, many=True)
        return Response(
            {
                "article": article_serializer.data,
                "multimedia": multimedia_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ListBookmarkedMediaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        bookmarked_articles = BookmarkMedia.objects.filter(
            multimedia=None, is_bookmarked=True
        )
        bookmarked_multimedias = BookmarkMedia.objects.filter(
            article=None, is_bookmarked=True
        )
        bookmarked_articles_unique_set = remove_duplicates(bookmarked_articles)
        bookmarked_multimedias_unique_set = remove_duplicates(bookmarked_multimedias)
        article_serializer = BookmarkMediaSerializer(
            bookmarked_articles_unique_set, many=True
        )
        multimedia_serializer = BookmarkMediaSerializer(
            bookmarked_multimedias_unique_set, many=True
        )
        return Response(
            {
                "article": article_serializer.data,
                "multimedia": multimedia_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ListPinnedMediaView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        pinned_articles = PinMedia.objects.filter(multimedia=None, is_pinned=True)
        pinned_multimedias = PinMedia.objects.filter(article=None, is_pinned=True)
        pinned_articles_unique_set = remove_duplicates(pinned_articles)
        pinned_multimedias_unique_set = remove_duplicates(pinned_multimedias)
        article_serializer = PinMediaSerializer(pinned_articles_unique_set, many=True)
        multimedia_serializer = PinMediaSerializer(
            pinned_multimedias_unique_set, many=True
        )
        return Response(
            {
                "article": article_serializer.data,
                "multimedia": multimedia_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
