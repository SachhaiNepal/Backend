from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import (Article, BookmarkMedia, Comment, Love,
                               Multimedia, PinMedia)
from multimedia.serializers.article_actions import (CommentPostSerializer,
                                                    CommentSerializer,
                                                    LoveSerializer)


class LovedArticlesList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        loved_articles = Love.objects.filter(multimedia=None)
        serializer = LoveSerializer(data=loved_articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleExtraStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        article = get_object_or_404(Article, pk=pk)
        love, created = Love.objects.get_or_create(article=article, lover=request.user)
        bookmark, created = BookmarkMedia.objects.get_or_create(
            article=article, marker=request.user
        )
        love_counts = Love.objects.filter(article=article, is_loved=True).count()
        return Response(
            {
                "loved": love.is_loved,
                "bookmarked": bookmark.is_bookmarked,
                "love_count": love_counts,
            },
            status=status.HTTP_200_OK,
        )


class CreateOrToggleLoveStatusOfArticle(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            article = Article.objects.get(pk=pk)
            love, created = Love.objects.get_or_create(
                article=article, lover=request.user
            )
            if created:
                love.is_loved = True
            else:
                love.is_loved = not love.is_loved
            love.save()
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


class MultimediaExtraStatus(APIView):
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
                "loved": love.is_loved,
                "bookmarked": bookmark.is_bookmarked,
                "pinned": pin.is_pinned,
                "love_count": love_count,
                "bookmark_count": bookmark_count,
                "pin_count": pin_count,
            },
            status=status.HTTP_200_OK,
        )


class CreateOrToggleLoveStatusOfMultimedia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
            love, created = Love.objects.get_or_create(
                multimedia=multimedia, lover=request.user
            )
            if created:
                love.is_loved = True
            else:
                love.is_loved = not love.is_loved
            love.save()
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


class ListArticleComments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        comments = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comments, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class ListMultimediaComments(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Multimedia, pk=pk)

    def get(self, request, pk):
        multimedia = self.get_object(pk)
        comments = Comment.objects.filter(multimedia=multimedia)
        serializer = CommentSerializer(comments, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class PostComment(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = CommentPostSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            print(request.user)
            # serializer.writer = request.user
            print(serializer)
            serializer.save()
            return Response(
                {"success": True, "comment": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOrTogglePinStatusOfMultimedia(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
            pin_media, created = PinMedia.objects.get_or_create(
                multimedia=multimedia, pinner=request.user
            )
            if created:
                pin_media.is_pinned = True
            else:
                pin_media.is_pinned = not pin_media.is_pinned
            pin_media.save()
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


class CreateOrTogglePinStatusOfArticle(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            article = Article.objects.get(pk=pk)
            pin_media, created = PinMedia.objects.get_or_create(
                article=article, pinner=request.user
            )
            if created:
                pin_media.is_pinned = True
            else:
                pin_media.is_pinned = not pin_media.is_pinned
            pin_media.save()
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
