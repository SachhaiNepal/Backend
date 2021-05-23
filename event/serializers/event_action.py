from rest_framework import serializers

from event.sub_models.event_action import EventComment, EventInterest


class EventCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComment
        fields = "__all__"


class EventInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInterest
        fields = "__all__"
