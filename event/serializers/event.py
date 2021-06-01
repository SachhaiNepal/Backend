from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from event.serializers.event_media import (EventPhotoSerializer,
                                           EventVideoSerializer,
                                           EventVideoUrlSerializer)
from event.sub_models.event import Event
from utils.file import check_size


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    @staticmethod
    def validate_banner(obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj

    # object level validation
    def validate(self, data):
        """
        Check if both vdc and municipality are selected
        """
        vdc = data.get("vdc")
        vdc_ward = data.get("vdc_ward")
        municipality = data.get("municipality")
        municipality_ward = data.get("municipality_ward")

        if not municipality and not vdc:
            raise serializers.ValidationError(
                "One of the municipality or vdc must be assigned."
            )
        if not municipality_ward and not vdc_ward:
            raise serializers.ValidationError(
                "One of the municipality or vdc ward must be assigned."
            )
        if municipality and vdc:
            raise serializers.ValidationError(
                "Both municipality and vdc cannot be assigned."
            )
        if municipality_ward and vdc_ward:
            raise serializers.ValidationError(
                "Both municipality or vdc ward cannot be assigned."
            )
        if municipality and vdc_ward:
            raise serializers.ValidationError(
                "Municipality and vdc ward is not an expected location combination."
            )
        if vdc and municipality_ward:
            raise serializers.ValidationError(
                "Vdc and municipality ward is not an expected location combination."
            )
        return data

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)


class EventSerializer(serializers.ModelSerializer):
    images = EventPhotoSerializer(many=True, read_only=True)
    video_urls = EventVideoUrlSerializer(many=True, read_only=True)
    videos = EventVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
        depth = 1
