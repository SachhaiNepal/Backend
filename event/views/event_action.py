from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from event.serializers.event_action import (EventCommentSerializer,
                                            EventInterestSerializer)
from event.sub_models.event import Event
from event.sub_models.event_action import EventComment, EventInterest


class EventCommentViewSet(viewsets.ModelViewSet):
    queryset = EventComment.objects.all()
    serializer_class = EventCommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["event"]


class EventInterestViewSet(viewsets.ModelViewSet):
    queryset = EventInterest.objects.all()
    serializer_class = EventInterestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["event", "going", "interested"]


class EventStatistics(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        event = get_object_or_404(Event, pk=pk)
        going_count = EventInterest.objects.filter(going=True, event=event).count()
        interested_count = EventInterest.objects.filter(
            interested=True, event=event
        ).count()
        return Response(
            {"going_count": going_count, "interested_count": interested_count},
            status=status.HTTP_201_CREATED,
        )


class ToggleEventInterestedStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        event = get_object_or_404(Event, pk=pk)
        user = request.user
        user_event_interest, created = EventInterest.objects.get_or_create(
            event=event, follower=user
        )
        if created:
            user_event_interest.interested = True
        else:
            user_event_interest.interested = not user_event_interest.interested
        user_event_interest.save()
        return Response(
            {"message": "Event interest toggled."}, status=status.HTTP_200_OK
        )


class ToggleEventGoingStatus(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        event = get_object_or_404(Event, pk=pk)
        user = request.user
        user_event_interest, created = EventInterest.objects.get_or_create(
            event=event, follower=user
        )
        if created:
            user_event_interest.going = True
        else:
            user_event_interest.going = not user_event_interest.going
        user_event_interest.save()
        return Response(
            {"message": "Event going status toggled."}, status=status.HTTP_200_OK
        )
