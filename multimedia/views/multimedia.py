from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from multimedia.models import Multimedia, MultimediaAudio, MultimediaImage, MultimediaVideo
from multimedia.serializers.model_serializer import MultimediaAudioSerializer, MultimediaImageSerializer, \
    MultimediaVideoSerializer
from multimedia.serializers.multimedia_list import AddMultimediaAudioListSerializer, AddMultimediaImageListSerializer, \
    AddMultimediaVideoListSerializer, MultimediaWithMultimediaListCreateSerializer
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


class CreateMultimediaWithMultimediaList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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


class ToggleMultimediaApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            multimedia = Multimedia.objects.get(pk=pk)
        except Multimedia.DoesNotExist:
            return Response({
                "detail": "Multimedia does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        multimedia.is_approved = not multimedia.is_approved
        if multimedia.is_approved:
            multimedia.approved_by = request.user
            multimedia.approved_at = timezone.now()
        else:
            multimedia.approved_by = None
            multimedia.approved_at = None
        multimedia.save()
        return Response({
            "message": "Multimedia {} successfully.".format("approved" if multimedia.is_approved else "rejected")
        }, status=status.HTTP_204_NO_CONTENT)
