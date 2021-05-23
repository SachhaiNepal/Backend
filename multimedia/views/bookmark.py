from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Article, BookmarkMedia, Multimedia


class CreateOrToggleBookmarkStatusOfArticle(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            article = Article.objects.get(pk=pk)
            bookmark, created = BookmarkMedia.objects.get_or_create(
                article=article, marker=request.user
            )
            if created:
                bookmark.is_bookmarked = True
            else:
                bookmark.is_bookmarked = not bookmark.is_bookmarked
            bookmark.save()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Article.DoesNotExist:
            return Response(
                {"detail": "Article not found."}, status=status.HTTP_404_NOT_FOUND
            )


class CreateOrToggleBookmarkStatusOfMultimedia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
            bookmark, created = BookmarkMedia.objects.get_or_create(
                multimedia=multimedia, marker=request.user
            )
            if created:
                bookmark.is_bookmarked = True
            else:
                bookmark.is_bookmarked = not bookmark.is_bookmarked
            bookmark.save()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Multimedia.DoesNotExist:
            return Response(
                {"detail": "Multimedia not found."}, status=status.HTTP_404_NOT_FOUND
            )
