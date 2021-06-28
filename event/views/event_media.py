from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from event.serializers.event_media import (EventPhotoSerializer,
                                           EventVideoSerializer,
                                           EventVideoUrlSerializer)
from event.serializers.event_media_list import (AddEventImageListSerializer,
                                                AddEventVideoListSerializer,
                                                AddEventVideoUrlListSerializer)
from event.sub_models.event_media import EventPhoto, EventVideo, EventVideoUrl


class EventPhotoViewSet(viewsets.ModelViewSet):
    queryset = EventPhoto.objects.all()
    serializer_class = EventPhotoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["event"]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        image = self.get_object()
        serializer = EventPhotoSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get("image"):
                image.image.delete()
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        event_photo = self.get_object()
        event_photo.image.delete()
        event_photo.delete()
        return Response(
            {"message": "Event image deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


class EventVideoUrlsViewSet(viewsets.ModelViewSet):
    queryset = EventVideoUrl.objects.all()
    serializer_class = EventVideoUrlSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["event"]


class EventVideoViewSet(viewsets.ModelViewSet):
    queryset = EventVideo.objects.all()
    serializer_class = EventVideoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["event"]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        video = self.get_object()
        serializer = EventVideoSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            if serializer.validated_data.get("video"):
                video.video.delete()
            if serializer.validated_data.get("poster"):
                video.poster.delete()
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        event_video = self.get_object()
        event_video.video.delete()
        if event_video.poster:
            event_video.poster.delete()
        event_video.delete()
        return Response(
            {"message": "Event video deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AddEventPhotoListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        serializer = AddEventImageListSerializer(
            data=request.data, context={"event_id": pk}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddEventVideoUrlsListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        serializer = AddEventVideoUrlListSerializer(
            data=request.data, context={"event_id": pk}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddEventVideoListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request, pk):
        serializer = AddEventVideoListSerializer(
            data=request.data, context={"event_id": pk}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
