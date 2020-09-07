import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Article, ArticleImage, Multimedia, MultimediaAudio, MultimediaVideo, MultimediaImage
from multimedia.serializers import ArticleImageSerializer, MultimediaAudioSerializer, MultimediaVideoSerializer, \
    MultimediaImageSerializer


def generate_url_for_media_resource(serializer, param):
    for target in serializer.data:
        front = "http" if os.getenv("IS_SECURE") else "https"
        target[param] = "{}://{}{}".format(front, os.getenv("BASE_URL"), target[param])
    return serializer


class ListArticleImages(APIView):
    @staticmethod
    def get(request, pk):
        try:
            article = Article.objects.get(pk=pk)
            images = ArticleImage.objects.filter(article=article)
            serializer = ArticleImageSerializer(images, many=True)
            serializer = generate_url_for_media_resource(serializer, "image")
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
            serializer = generate_url_for_media_resource(serializer, "audio")
            return Response({
                "count": multimedia_audios.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Multimedia.DoesNotExist:
            return Response({
                "details": "Multimedia not found."
            }, status=status.HTTP_404_NOT_FOUND)


class ListMultimediaImages(APIView):
    @staticmethod
    def get(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
            multimedia_images = MultimediaImage.objects.filter(multimedia=multimedia)
            serializer = MultimediaImageSerializer(multimedia_images, many=True)
            serializer = generate_url_for_media_resource(serializer, "image")
            return Response({
                "count": multimedia_images.count(),
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
            serializer = generate_url_for_media_resource(serializer, "video")
            return Response({
                "count": multimedia_videos.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Multimedia.DoesNotExist:
            return Response({
                "details": "Multimedia not found."
            }, status=status.HTTP_404_NOT_FOUND)
