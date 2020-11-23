from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from event.models import Event, EventPhoto, EventVideoUrls
from event.serializers import EventSerializer, EventPhotoSerializer, EventVideoUrlsSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = (MultiPartParser, FormParser,)
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        event.banner.delete()
        event.delete()
        return Response({
            "message": "Event deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class EventPhotoViewSet(viewsets.ModelViewSet):
    queryset = EventPhoto.objects.all()
    serializer_class = EventPhotoSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def destroy(self, request, *args, **kwargs):
        event_photo = self.get_object()
        event_photo.image.delete()
        event_photo.delete()
        return Response({
            "message": "Event photo deleted successfully"
        }, status=status.HTTP_204_NO_CONTENT)


class EventVideoUrlsViewSet(viewsets.ModelViewSet):
    queryset = EventVideoUrls.objects.all()
    serializer_class = EventVideoUrlsSerializer
