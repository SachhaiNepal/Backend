from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.serializers.article_list import ArticleWithImageListCreateSerializer
from multimedia.serializers.multimedia_list import MultimediaWithMultimediaListCreateSerializer


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


class CreateMultimediaWithMultimediaList(APIView):
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser,)

    @staticmethod
    def post(request):
        if request.user.is_anonymous:
            return Response({
                "details": "User must be logged in.",
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = MultimediaWithMultimediaListCreateSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Multimedia Created Successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
