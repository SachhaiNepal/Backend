import os

from rest_framework import permissions, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Multimedia, MultimediaVideo, MultimediaAudio, Article, ArticleImage
from multimedia.serializers import MultimediaSerializer, MultimediaVideoSerializer, \
    MultimediaAudioSerializer, ArticleSerializer, ArticleImageSerializer, ArticleWithImageListSerializer, \
    MultimediaWithMultimediaListSerializer


class MultimediaViewSet(viewsets.ModelViewSet):
    queryset = Multimedia.objects.all()
    serializer_class = MultimediaSerializer
    permission_classes = [permissions.IsAdminUser]


class MultimediaVideoViewSet(viewsets.ModelViewSet):
    queryset = MultimediaVideo.objects.all()
    serializer_class = MultimediaVideoSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class MultimediaAudioViewSet(viewsets.ModelViewSet):
    queryset = MultimediaAudio.objects.all()
    serializer_class = MultimediaAudioSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAdminUser]


class ArticleImageViewSet(viewsets.ModelViewSet):
    queryset = ArticleImage.objects.all()
    serializer_class = ArticleImageSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class CreateArticleWithImageList(APIView):
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        if request.user.is_anonymous:
            return Response({
                "details": "User must be logged in.",
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleWithImageListSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Article Created Successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateMultimediaWithMultimediaList(APIView):
    authentication_classes = [TokenAuthentication]
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request):
        if request.user.is_anonymous:
            return Response({
                "details": "User must be logged in.",
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = MultimediaWithMultimediaListSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Multimedia Created Successfully."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListArticleImages(APIView):
    @staticmethod
    def get(request, pk):
        try:
            article = Article.objects.get(pk=pk)
            images = ArticleImage.objects.filter(article=article)
            serializer = ArticleImageSerializer(images, many=True)
            for target in serializer.data:
                front = "http" if os.getenv("IS_SECURE") else "https"
                target["image"] = "{}://{}{}".format(front, os.getenv("BASE_URL"), target["image"])
                print(target["image"])
            return Response({
                "count": images.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response({
                "details": "Article not found."
            }, status=status.HTTP_404_NOT_FOUND)


class ListMultimediaAudios(APIView):
    @staticmethod
    def get(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
            multimedia_audios = MultimediaAudio.objects.filter(multimedia=multimedia)
            serializer = MultimediaAudioSerializer(multimedia_audios, many=True)
            for target in serializer.data:
                front = "http" if os.getenv("IS_SECURE") else "https"
                target["audio"] = "{}://{}{}".format(front, os.getenv("BASE_URL"), target["audio"])
                print(target["audio"])
            return Response({
                "count": multimedia_audios.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Multimedia.DoesNotExist:
            return Response({
                "details": "Multimedia not found."
            }, status=status.HTTP_404_NOT_FOUND)


class ListMultimediaVideos(APIView):
    @staticmethod
    def get(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
            multimedia_videos = MultimediaVideo.objects.filter(multimedia=multimedia)
            serializer = MultimediaVideoSerializer(multimedia_videos, many=True)
            for target in serializer.data:
                front = "http" if os.getenv("IS_SECURE") else "https"
                target["video"] = "{}://{}{}".format(front, os.getenv("BASE_URL"), target["video"])
                print(target["video"])
            return Response({
                "count": multimedia_videos.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Multimedia.DoesNotExist:
            return Response({
                "details": "Multimedia not found."
            }, status=status.HTTP_404_NOT_FOUND)
