from django.core.validators import RegexValidator
from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from event.sub_models.event_media import EventPhoto, EventVideoUrls
from utils.file import check_size


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
