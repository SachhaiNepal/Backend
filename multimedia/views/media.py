from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from multimedia.models import MultimediaAudio, MultimediaImage, MultimediaVideo
from multimedia.serializers.multimedia import (MultimediaAudioSerializer,
                                               MultimediaImageSerializer,
                                               MultimediaVideoSerializer)
from multimedia.sub_models.media import MultimediaVideoUrl


class MultimediaImageViewSet(viewsets.ModelViewSet):
    queryset = MultimediaImage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MultimediaImageSerializer
    filterset_fields = ["multimedia"]

    def delete(self, request, pk):
        multimedia_image = self.get_object(pk)
        multimedia_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MultimediaAudioViewSet(viewsets.ModelViewSet):
    queryset = MultimediaAudio.objects.all()
    serializer_class = MultimediaAudioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    filterset_fields = ["multimedia"]

    def delete(self, request, pk):
        multimedia_audio = self.get_object(pk)
        multimedia_audio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MultimediaVideoViewSet(viewsets.ModelViewSet):
    queryset = MultimediaVideo.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MultimediaVideoSerializer
    filterset_fields = ["multimedia"]

    def delete(self, request, pk):
        multimedia_video = self.get_object(pk)
        multimedia_video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MultimediaVideoUrlViewSet(viewsets.ModelViewSet):
    queryset = MultimediaVideoUrl.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = MultimediaVideoSerializer
    filterset_fields = ["multimedia"]
