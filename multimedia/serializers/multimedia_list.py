from django.core.validators import RegexValidator
from rest_framework import serializers

from multimedia.models import (Multimedia, MultimediaAudio, MultimediaImage,
                               MultimediaVideo, MultimediaVideoUrls)
from utils.file import (check_audio_size_with_ext, check_image_size_with_ext,
                        check_video_size_with_ext)
from utils.helper import get_keys_from_ordered_dict


class UpdateMultimediaImageListSerializer(serializers.Serializer):
    image = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=True), required=True
    )

    def validate_image(self, obj):
        check_image_size_with_ext(obj)
        return obj

    def create(self, validated_data):
        multimedia_id = self.context["multimedia_id"]
        images = validated_data.pop("image")

        multimedia = Multimedia.objects.get(pk=multimedia_id)
        for image in images:
            multimedia, created = MultimediaImage.objects.get_or_create(
                image=image, multimedia=multimedia, **validated_data
            )
        return UpdateMultimediaImageListSerializer(**validated_data)


class UpdateMultimediaAudioListSerializer(serializers.Serializer):
    audio = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=False,
        ),
        required=True,
    )

    def validate_audio(self, obj):
        check_audio_size_with_ext(obj)
        return obj

    def create(self, validated_data):
        multimedia_id = self.context["multimedia_id"]
        audios = validated_data.pop("audio")

        multimedia = Multimedia.objects.get(id=multimedia_id)
        for audio in audios:
            multimedia, created = MultimediaAudio.objects.get_or_create(
                audio=audio,
                multimedia=multimedia,
            )
        return UpdateMultimediaAudioListSerializer(**validated_data)


class UpdateMultimediaVideoListSerializer(serializers.Serializer):
    video = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        required=False,
    )

    def validate_video(self, obj):
        check_video_size_with_ext(obj)
        return obj

    def create(self, validated_data):
        multimedia_id = self.context["multimedia_id"]
        videos = validated_data.pop("video")

        multimedia = Multimedia.objects.get(pk=multimedia_id)
        for video in videos:
            multimedia, created = MultimediaVideo.objects.get_or_create(
                video=video, multimedia=multimedia, **validated_data
            )
        return UpdateMultimediaVideoListSerializer(**validated_data)


class CreateMultimediaWithMultimediaListSerializer(serializers.Serializer):
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

    audio = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=False,
        ),
        required=False,
    )
    image = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=False,
            use_url=False,
        ),
        required=False,
    )
    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=True, max_length=512)

    def validate_title(self, title):
        try:
            Multimedia.objects.get(title=title)
            raise serializers.ValidationError("Multimedia title must be unique.")
        except Multimedia.DoesNotExist:
            return title

    def validate_description(self, description):
        try:
            Multimedia.objects.get(description=description)
            raise serializers.ValidationError("Multimedia description must be unique.")
        except Multimedia.DoesNotExist:
            return description

    def validate_image(self, obj):
        check_image_size_with_ext(obj)
        return obj

    def validate_video(self, obj):
        check_video_size_with_ext(obj)
        return obj

    def validate_audio(self, obj):
        check_audio_size_with_ext(obj)
        return obj

    def create(self, validated_data):
        keys = get_keys_from_ordered_dict(validated_data)
        user = self.context["request"].user
        title = validated_data.pop("title")
        description = validated_data.pop("description")

        multimedia, created = Multimedia.objects.get_or_create(
            title=title,
            description=description,
            uploaded_by=user,
        )
        if not created:
            raise serializers.ValidationError(
                {
                    "message": "ACCESS DENIED",
                    "detail": "Multimedia already exists.",
                }
            )

        if "video" in keys:
            videos = validated_data.pop("video")
            for video in videos:
                MultimediaVideo.objects.create(
                    video=video,
                    multimedia=multimedia,
                )

        if "video_url" in keys:
            video_urls = validated_data.pop("video_url")
            for video_url in video_urls:
                MultimediaVideoUrls.objects.create(
                    video_url=video_url,
                    multimedia=multimedia,
                )

        if "audio" in keys:
            audios = validated_data.pop("audio")
            for audio in audios:
                MultimediaAudio.objects.create(
                    audio=audio,
                    multimedia=multimedia,
                )

        if "image" in keys:
            images = validated_data.pop("image")
            for image in images:
                MultimediaImage.objects.create(
                    image=image,
                    multimedia=multimedia,
                )
        return CreateMultimediaWithMultimediaListSerializer(**validated_data)
