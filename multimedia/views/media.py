from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from multimedia.models import Sound, Image, Video
from multimedia.serializers.media import VideoUrlSerializer, ImageSerializer, AudioSerializer, VideoSerializer
from multimedia.sub_models.media import VideoUrl


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ImageSerializer
    filterset_fields = ["multimedia"]

    def delete(self, request, pk):
        multimedia_image = self.get_object(pk)
        multimedia_image.image.delete()
        multimedia_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SoundViewSet(viewsets.ModelViewSet):
    queryset = Sound.objects.all()
    serializer_class = AudioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filterset_fields = ["multimedia"]

    def delete(self, request, pk):
        multimedia_audio = self.get_object(pk)
        multimedia_audio.sound.delete()
        multimedia_audio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VideoSerializer
    filterset_fields = ["multimedia"]

    def delete(self, request, pk):
        multimedia_video = self.get_object(pk)
        multimedia_video.video.delete()
        multimedia_video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoUrlViewSet(viewsets.ModelViewSet):
    queryset = VideoUrl.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["multimedia"]
    serializer_class = VideoUrlSerializer
