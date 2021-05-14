from django.core.validators import RegexValidator
from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from event.models import Event, EventPhoto, EventVideoUrls
from utils.file import check_size


class EventPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def validate_banner(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj

    # object level validation
    def validate(self, data):
        """
        Check if both vdc and municipality are selected
        """
        try:
            check = data["municipality"]
            try:
                check = data["vdc"]
                raise serializers.ValidationError(
                    "Both municipality and vdc cannot be assigned."
                )
            except KeyError:
                return data
        except KeyError:
            try:
                check = data["vdc"]
                return data
            except KeyError:
                raise serializers.ValidationError(
                    "One of the municipality or vdc must be assigned."
                )

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
        depth = 1


class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = "__all__"

    def validate_image(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj


class EventVideoUrlsSerializer(serializers.ModelSerializer):
    video_urls = serializers.ListField(
        child=serializers.URLField(
            validators=[
                RegexValidator(
                    regex=r"https:\/\/www\.youtube\.com\/*",
                    message="URL must be sourced from youtube.",
                )
            ]
        )
    )

    class Meta:
        model = EventVideoUrls
        fields = "__all__"
