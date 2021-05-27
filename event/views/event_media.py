from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
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
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    filterset_fields = ["event"]

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
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    filterset_fields = ["event"]

    def destroy(self, request, *args, **kwargs):
        event_video = self.get_object()
        event_video.video.delete()
        event_video.delete()
        return Response(
            {"message": "Event video deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AddEventPhotoListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        serializer = AddEventImageListSerializer(
            data=request.data, context={"event_id": pk}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Images list added."}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddEventVideoUrlsListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        serializer = AddEventVideoUrlListSerializer(
            data=request.data, context={"event_id": pk}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Video urls list added."}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddEventVideoListView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        serializer = AddEventVideoListSerializer(
            data=request.data, context={"event_id": pk}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Videos list added."}, status=status.HTTP_204_NO_CONTENT
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
