from rest_framework import authentication, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import ArticleImage, MultimediaVideo, MultimediaImage, MultimediaAudio
from multimedia.serializers.model_serializer import ArticleImageSerializer, MultimediaImageSerializer, \
    MultimediaAudioSerializer, MultimediaVideoSerializer
from utils.helper import generate_url_for_media_resource


class ArticleImageDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(ArticleImage, pk=pk)

    def get(self, request, pk):
        article_image = self.get_object(pk)
        serializer = ArticleImageSerializer(article_image)
        serializer = generate_url_for_media_resource(serializer.data, "image")
        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        article_image = self.get_object(pk)
        article_image.delete()
        return Response({
            "detail": "Article image deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class MultimediaImageDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(MultimediaImage, pk=pk)

    def get(self, request, pk):
        multimedia_image = self.get_object(pk)
        serializer = MultimediaImageSerializer(multimedia_image)
        serializer = generate_url_for_media_resource(serializer.data, "image")
        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        multimedia_image = self.get_object(pk)
        multimedia_image.delete()
        return Response({
            "detail": "Multimedia image deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class MultimediaAudioDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(MultimediaAudio, pk=pk)

    def get(self, request, pk):
        multimedia_audio = self.get_object(pk)
        serializer = MultimediaAudioSerializer(multimedia_audio)
        serializer = generate_url_for_media_resource(serializer.data, "audio")
        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        multimedia_audio = self.get_object(pk)
        multimedia_audio.delete()
        return Response({
            "detail": "Multimedia audio deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class MultimediaVideoDetailView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(MultimediaVideo, pk=pk)

    def get(self, request, pk):
        multimedia_video = self.get_object(pk)
        serializer = MultimediaVideoSerializer(multimedia_video)
        serializer = generate_url_for_media_resource(serializer.data, "video")
        return Response(serializer, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        multimedia_video = self.get_object(pk)
        multimedia_video.delete()
        return Response({
            "detail": "Multimedia video deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
