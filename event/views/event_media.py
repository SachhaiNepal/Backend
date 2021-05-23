from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from event.serializers.event_media import EventPhotoSerializer, EventVideoUrlsSerializer
from event.sub_models.event_media import EventPhoto, EventVideoUrls


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
            {"message": "Event photo deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class EventVideoUrlsViewSet(viewsets.ModelViewSet):
    queryset = EventVideoUrls.objects.all()
    serializer_class = EventVideoUrlsSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["event"]
