from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.serializers.action import (BookmarkThinSerializer,
                                           LoveThinSerializer)
from multimedia.serializers.multimedia import MultimediaPOSTSerializer
from multimedia.sub_models.action import Bookmark, Love
from multimedia.sub_models.multimedia import Multimedia


class ApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        if not multimedia.is_approved:
            multimedia.is_approved = True
            multimedia.approved_by = request.user
            multimedia.approved_at = timezone.now()
            multimedia.save()
            return Response(
                MultimediaPOSTSerializer(multimedia).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            MultimediaPOSTSerializer(multimedia).data, status=status.HTTP_200_OK
        )

    @staticmethod
    def delete(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        if multimedia.is_approved:
            multimedia.is_approved = False
            multimedia.approved_by = None
            multimedia.approved_at = None
            multimedia.save()
        return Response(
            MultimediaPOSTSerializer(multimedia).data, status=status.HTTP_200_OK
        )


class BookmarkView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(
            multimedia=multimedia, marker=request.user
        )
        if created or not bookmark.is_bookmarked:
            bookmark.is_bookmarked = True
            bookmark.save()
        return Response(
            BookmarkThinSerializer(bookmark).data, status=status.HTTP_201_CREATED
        )

    @staticmethod
    def delete(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        bookmark, created = Bookmark.objects.get_or_create(
            multimedia=multimedia, marker=request.user
        )
        if not created or bookmark.is_bookmarked:
            bookmark.is_bookmarked = False
            bookmark.save()
        return Response(
            BookmarkThinSerializer(bookmark).data, status=status.HTTP_200_OK
        )


class LoveView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        love, created = Love.objects.get_or_create(
            multimedia=multimedia, lover=request.user
        )
        if created or not love.is_loved:
            love.is_loved = True
            love.save()
        return Response(LoveThinSerializer(love).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        love, created = Love.objects.get_or_create(
            multimedia=multimedia, lover=request.user
        )
        if not created or love.is_loved:
            love.is_loved = False
            love.save()
        return Response(LoveThinSerializer(love).data, status=status.HTTP_200_OK)


class PinView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        multimedia.is_pinned = True
        multimedia.pinner = request.user
        multimedia.save()
        return Response(
            MultimediaPOSTSerializer(multimedia).data, status=status.HTTP_204_NO_CONTENT
        )

    @staticmethod
    def delete(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        multimedia.is_pinned = False
        multimedia.pinner = None
        multimedia.save()
        return Response(
            MultimediaPOSTSerializer(multimedia).data, status=status.HTTP_204_NO_CONTENT
        )


class MultimediaStatusForMe(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        multimedia = get_object_or_404(Multimedia, pk=pk)
        love, created = Love.objects.get_or_create(
            multimedia=multimedia, lover=request.user
        )
        bookmark, created = Bookmark.objects.get_or_create(
            multimedia=multimedia, marker=request.user
        )
        loves = Love.objects.filter(multimedia=multimedia, is_loved=True)
        bookmarks = Bookmark.objects.filter(multimedia=multimedia, is_bookmarked=True)
        return Response(
            {
                "loved": love.is_loved,
                "bookmarked": bookmark.is_bookmarked,
                "love_count": loves.count(),
                "bookmark_count": bookmarks.count(),
            },
            status=status.HTTP_200_OK,
        )
