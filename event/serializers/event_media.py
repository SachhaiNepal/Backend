from django.core.validators import RegexValidator
from rest_framework import serializers

from event.sub_models.event_media import EventPhoto, EventVideo, EventVideoUrl
from utils.file import check_video_size_with_ext, check_image_size_with_ext
from utils.helper import get_youtube_video_data


class EventVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventVideo
        fields = "__all__"

    @staticmethod
    def validate_video(obj):
        check_video_size_with_ext(obj)
        return obj


class EventPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventPhoto
        fields = "__all__"

    @staticmethod
    def validate_image(obj):
        check_image_size_with_ext(obj)
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


class EventVideoListSerializer(serializers.ModelSerializer):
    yt_info = serializers.SerializerMethodField()

    @staticmethod
    def get_yt_info(obj):
        return get_youtube_video_data(obj.video_url)

    class Meta:
        model = EventVideoUrl
        fields = ["id", "video_url", "yt_info", "event"]
