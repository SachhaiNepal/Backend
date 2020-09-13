from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Multimedia, MultimediaAudio, MultimediaImage, MultimediaVideo
from multimedia.serializers.model_serializer import MultimediaAudioSerializer, MultimediaImageSerializer, \
    MultimediaVideoSerializer
from multimedia.serializers.multimedia_list import AddMultimediaAudioListSerializer, AddMultimediaImageListSerializer, \
    AddMultimediaVideoListSerializer
from utils.helper import generate_url_for_media_resources


class ListMultimediaAudios(APIView):
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
        return Response({
            "count": multimedia_audios.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Adds multiple audios to a multimedia
        """
        multimedia = self.get_object(pk)
        context = {
            "multimedia_id": multimedia.pk
        }
        serializer = AddMultimediaAudioListSerializer(data=request.data, context=context)
        if serializer.is_valid():
            return Response({
                "details": "Audios added to multimedia successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMultimediaImages(APIView):
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
        return Response({
            "count": multimedia_images.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Adds multiple images to a multimedia
        """
        multimedia = self.get_object(pk)
        context = {
            "multimedia_id": multimedia.pk
        }
        serializer = AddMultimediaImageListSerializer(data=request.data, context=context)
        if serializer.is_valid():
            return Response({
                "details": "Images added to multimedia successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMultimediaVideos(APIView):
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
        return Response({
            "count": multimedia_videos.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Adds multiple videos to a multimedia
        """
        multimedia = self.get_object(pk)
        context = {
            "multimedia_id": multimedia.pk
        }
        serializer = AddMultimediaVideoListSerializer(data=request.data, context=context)
        if serializer.is_valid():
            return Response({
                "details": "Videos added to multimedia successfully."
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
