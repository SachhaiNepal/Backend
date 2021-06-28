from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from event.serializers.event import (EventBannerImageSerializer,
                                     EventPostSerializer, EventSerializer)
from event.sub_models.event import Event, EventBannerImage
from event.sub_models.event_media import EventPhoto, EventVideo


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("-created_at")
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["branch", "is_approved"]
    search_fields = ["title", "description", "created_by__username"]

    def get_serializer_class(self):
        if self.action not in ["list", "retrieve"]:
            return EventPostSerializer
        return super(EventViewSet, self).get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        event_banner = EventBannerImage.objects.filter(event=event)
        [image.delete() for image in event_banner]
        event_images = EventPhoto.objects.filter(event=event)
        [image.delete() for image in event_images]
        event_videos = EventVideo.objects.filter(event=event)
        [video.delete() for video in event_videos]
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleEventApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request, pk):
        event = get_object_or_404(Event, pk=pk)
        if not event.is_approved:
            event.is_approved = True
            event.approved_by = request.user
            event.approved_at = timezone.now()
            event.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk):
        event = get_object_or_404(Event, pk=pk)
        if event.is_approved:
            event.is_approved = False
            event.approved_by = None
            event.approved_at = None
            event.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventBannerImageViewSet(viewsets.ModelViewSet):
    queryset = EventBannerImage.objects.all()
    serializer_class = EventBannerImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["event"]

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        event_banner = self.get_object()
        event_banner.image.delete()
        event_banner.delete()
        return Response(
            {"message": "Event banner image deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )
