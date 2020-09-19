from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.serializers.article_list import *
from utils.helper import generate_url_for_media_resources
from multimedia.serializers.model_serializer import ArticleImageSerializer


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


class CreateArticleWithImageList(APIView):
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser,)

    @staticmethod
    def post(request):
        if request.user.is_anonymous:
            return Response({
                "details": "User must be logged in.",
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleWithImageListCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Article Created Successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
