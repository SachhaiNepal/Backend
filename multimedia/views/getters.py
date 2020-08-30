import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Article, ArticleImage, Multimedia, MultimediaAudio, MultimediaVideo
from multimedia.serializers import ArticleImageSerializer, MultimediaAudioSerializer, MultimediaVideoSerializer


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
