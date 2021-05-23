from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Article, ArticleImage
from multimedia.serializers.article import ArticleImageSerializer


class ListArticleImages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        """
        Returns list of images for an article
        """
        context = {"request": request}
        article = self.get_object(pk)
        images = ArticleImage.objects.filter(article=article)
        serializer = ArticleImageSerializer(images, many=True, context=context)
        return Response(
            {"count": images.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class ArticleImageDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(ArticleImage, pk=pk)

    def get(self, request, pk):
        context = {"request": request}
        article_image = self.get_object(pk)
        serializer = ArticleImageSerializer(article_image, context=context)
        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        article_image = self.get_object(pk)
        article_image.delete()
        return Response(
            {"success": True},
            status=status.HTTP_204_NO_CONTENT,
        )
