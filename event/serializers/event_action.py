from rest_framework import serializers

from event.sub_models.event_action import EventComment, EventInterest


class EventCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComment
        fields = "__all__"
        depth = 1


class EventCommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventComment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["writer"] = self.context["request"].user
        return EventComment.objects.create(**validated_data)


class EventInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventInterest
        fields = "__all__"
