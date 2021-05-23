from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import (Multimedia, MultimediaAudio, MultimediaImage,
                               MultimediaVideo, MultimediaVideoUrls)
from multimedia.serializers.multimedia import (MultimediaAudioSerializer,
                                               MultimediaImageSerializer,
                                               MultimediaVideoSerializer,
                                               MultimediaVideoUrlsSerializer)
from utils.helper import generate_url_for_media_resources


class ListMultimediaAudios(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Multimedia, pk=pk)

    def get(self, request, pk):
        """
        Returns list of audios for an multimedia
        """
        multimedia = self.get_object(pk)
        multimedia_audios = MultimediaAudio.objects.filter(multimedia=multimedia)
        serializer = MultimediaAudioSerializer(multimedia_audios, many=True)
        serializer = generate_url_for_media_resources(serializer, "audio")
        return Response(
            {"count": multimedia_audios.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class ListMultimediaVideoUrls(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Multimedia, pk=pk)

    def get(self, request, pk):
        """
        Returns list of images for a multimedia
        """
        multimedia = self.get_object(pk)
        multimedia_video_urls = MultimediaVideoUrls.objects.filter(
            multimedia=multimedia
        )
        serializer = MultimediaVideoUrlsSerializer(multimedia_video_urls, many=True)
        return Response(
            {"count": multimedia_video_urls.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class ListMultimediaImages(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Multimedia, pk=pk)

    def get(self, request, pk):
        """
        Returns list of images for a multimedia
        """
        multimedia = self.get_object(pk)
        multimedia_images = MultimediaImage.objects.filter(multimedia=multimedia)
        serializer = MultimediaImageSerializer(multimedia_images, many=True)
        serializer = generate_url_for_media_resources(serializer, "image")
        return Response(
            {"count": multimedia_images.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class ListMultimediaVideos(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Multimedia, pk=pk)

    def get(self, request, pk):
        """
        Returns list of videos for a multimedia
        """
        multimedia = self.get_object(pk)
        multimedia_videos = MultimediaVideo.objects.filter(multimedia=multimedia)
        serializer = MultimediaVideoSerializer(multimedia_videos, many=True)
        serializer = generate_url_for_media_resources(serializer, "video")
        return Response(
            {"count": multimedia_videos.count(), "data": serializer.data},
            status=status.HTTP_200_OK,
        )
