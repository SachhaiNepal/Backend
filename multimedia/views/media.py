from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from multimedia.models import Image, Sound, Video
from multimedia.serializers.media import (AudioSerializer, ImageSerializer,
                                          VideoSerializer, VideoUrlSerializer)
from multimedia.sub_models.media import VideoUrl


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    filterset_fields = ["multimedia"]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        image = self.get_object()
        serializer = ImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get("image"):
                image.image.delete()
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        multimedia_image = self.get_object()
        multimedia_image.image.delete()
        multimedia_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SoundViewSet(viewsets.ModelViewSet):
    queryset = Sound.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filterset_fields = ["multimedia"]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        sound = self.get_object()
        serializer = AudioSerializer(sound, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get("sound"):
                sound.sound.delete()
            if serializer.validated_data.get("poster"):
                sound.poster.delete()
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        multimedia_audio = self.get_object()
        if multimedia_audio.poster:
            multimedia_audio.poster.delete()
        multimedia_audio.sound.delete()
        multimedia_audio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VideoSerializer
    filterset_fields = ["multimedia"]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        video = self.get_object()
        serializer = VideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get("video"):
                video.video.delete()
            if serializer.validated_data.get("poster"):
                video.poster.delete()
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        multimedia_video = self.get_object()
        if multimedia_video.poster:
            multimedia_video.poster.delete()
        multimedia_video.video.delete()
        multimedia_video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoUrlViewSet(viewsets.ModelViewSet):
    queryset = VideoUrl.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["multimedia"]
    serializer_class = VideoUrlSerializer

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
