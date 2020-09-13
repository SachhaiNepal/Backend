from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Article, ArticleImage
from multimedia.serializers.article_list import AddArticleImageListSerializer
from multimedia.serializers.model_serializer import ArticleImageSerializer
from utils.helper import generate_url_for_media_resources


class ListArticleImages(APIView):
    @staticmethod
    def get_object(pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        """
        Returns list of images for an article
        """
        article = self.get_object(pk)
        images = ArticleImage.objects.filter(article=article)
        serializer = ArticleImageSerializer(images, many=True)
        serializer = generate_url_for_media_resources(serializer, "image")
        return Response({
            "count": images.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Adds list of images to an article
        """
        article = self.get_object(pk)
        context = {
            "article_id": article.pk
        }
        serializer = AddArticleImageListSerializer(data=request.data, context=context)
        if serializer.is_valid():
            return Response({
                "details": "Images added to article successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
