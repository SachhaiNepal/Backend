from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from event.serializers.event import (EventBannerImageSerializer,
                                     EventPostSerializer, EventSerializer)
from event.sub_models.event import Event, EventBannerImage


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("-created_at")
    serializer_class = EventSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ["branch", "is_approved"]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return EventPostSerializer
        return super(EventViewSet, self).get_serializer_class()


class ToggleEventApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        event.is_approved = not event.is_approved
        if event.is_approved:
            event.approved_by = request.user
            event.approved_at = timezone.now()
        else:
            event.approved_by = None
            event.approved_at = None
        event.save()
        return Response(
            {
                "message": "Event {} successfully.".format(
                    "approved" if event.is_approved else "rejected"
                )
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class EventBannerImageViewSet(viewsets.ModelViewSet):
    queryset = EventBannerImage.objects.all()
    serializer_class = EventBannerImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["event"]

    def destroy(self, request, *args, **kwargs):
        event_banner = self.get_object()
        event_banner.image.delete()
        event_banner.delete()
        return Response(
            {"message": "Event banner image deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )
