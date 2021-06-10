from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from event.serializers.event_media import (EventPhotoSerializer,
                                           EventVideoListSerializer,
                                           EventVideoSerializer)
from event.sub_models.event import Event, EventBannerImage
from utils.file import check_size
from utils.validate_location import validate_location


class EventBannerImageSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_image(obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj

    class Meta:
        model = EventBannerImage
        fields = "__all__"


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    # object level validation
    def validate(self, data):
        """
        Check if both vdc and municipality are selected
        """
        return validate_location(data)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)


class EventSerializer(serializers.ModelSerializer):
    banner_images = EventBannerImageSerializer(many=True, read_only=True)
    images = EventPhotoSerializer(many=True, read_only=True)
    video_urls = EventVideoListSerializer(many=True, read_only=True)
    videos = EventVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
        depth = 1
