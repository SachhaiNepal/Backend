from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from article.serializers.action import BookmarkSerializer
from article.sub_models.action import Love
from multimedia.serializers.action import LoveSerializer
from multimedia.sub_models.action import Bookmark


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


class ListLovedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        context = {"request": request}
        loved_articles = Love.objects.filter(is_loved=True)
        loved_articles_unique_set = remove_duplicates(loved_articles)
        article_serializer = LoveSerializer(
            loved_articles_unique_set, many=True, context=context
        )
        return Response(
            article_serializer.data,
            status=status.HTTP_200_OK,
        )


class ListBookmarkedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        context = {"request": request}
        bookmarked_articles = Bookmark.objects.filter(is_bookmarked=True)
        bookmarked_articles_unique_set = remove_duplicates(bookmarked_articles)
        article_serializer = BookmarkSerializer(
            bookmarked_articles_unique_set, many=True, context=context
        )
        return Response(
            article_serializer.data,
            status=status.HTTP_200_OK,
        )
