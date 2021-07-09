from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from multimedia.models import Multimedia
from utils.file import (check_audios_size_with_ext, check_images_size_with_ext,
                        check_videos_size_with_ext)


class MultimediaWithMediaListSerializer(serializers.Serializer):
    title = serializers.CharField(
        required=True,
        max_length=255,
        validators=[UniqueValidator(queryset=Multimedia.objects.all())],
    )
    description = serializers.CharField(required=False, allow_null=True, max_length=10000)
    image = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=False,
            use_url=False,
        ),
        required=False,
    )
    video = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        required=False,
    )
    video_url = serializers.ListField(
        child=serializers.URLField(
            validators=[
                RegexValidator(
                    regex=r"https:\/\/www\.youtube\.com\/*",
                    message="URL must be sourced from youtube.",
                )
            ]
        ),
        required=False,
    )

    sound = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=False,
        ),
        required=False,
    )

    @staticmethod
    def validate_image(obj):
        check_images_size_with_ext(obj)
        return obj

    @staticmethod
    def validate_video(obj):
        check_videos_size_with_ext(obj)
        return obj

    @staticmethod
    def validate_sound(obj):
        check_audios_size_with_ext(obj)
        return obj

    def validate(self, data):
        videos = data.get("video")
        images = data.get("image")
        url = data.get("video_url")
        sound = data.get("sound")
        if not videos and not images and not url and not sound:
            raise ValidationError("Please add at least a media for your multimedia.")
        if videos:
            if len(videos) > 0 and not images:
                raise ValidationError(
                    "Please add at least a image as thumbnail for your video resources."
                )
        return data
