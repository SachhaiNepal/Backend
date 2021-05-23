from django.core.validators import RegexValidator
from rest_framework import serializers

from backend.settings import (ALLOWED_VIDEO_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE,
                              MAX_UPLOAD_VIDEO_SIZE)
from event.sub_models.event_media import EventPhoto, EventVideo, EventVideoUrl
from utils.file import check_extension, check_size


class EventVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVideo
        fields = "__all__"

    def validate_video(self, obj):
        check_size(obj, MAX_UPLOAD_VIDEO_SIZE)
        check_extension(obj, ALLOWED_VIDEO_EXTENSIONS)
        return obj


class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = "__all__"

    def validate_image(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj


class EventVideoUrlSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[
            RegexValidator(
                regex=r"https:\/\/www\.youtube\.com\/*",
                message="URL must be sourced from youtube.",
            )
        ]
    )

    class Meta:
        model = EventVideoUrl
        fields = "__all__"
