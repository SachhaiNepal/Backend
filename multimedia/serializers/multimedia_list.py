from django.db import IntegrityError
from rest_framework import serializers, status

from multimedia.models import Multimedia, MultimediaVideo, MultimediaAudio, MultimediaImage
from utils.file import check_image_size, check_audio_size, check_video_size


class MultimediaWithMultimediaListSerializer(serializers.Serializer):
    video = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=False
        ),
        required=False
    )
    audio = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=False,
        ),
        required=False
    )
    image = serializers.ListField(
        child=serializers.ImageField(
            allow_empty_file=False,
            use_url=False,
        ),
        required=False
    )
    title = serializers.CharField(required=True, max_length=512)
    description = serializers.CharField(required=True, max_length=1024)

    def validate(self, data):
        check_image_size(data["image"])
        check_audio_size(data["audio"])
        check_video_size(data["video"])

    def create(self, validated_data):
        user = self.context["request"].user
        title = validated_data.pop("title")
        description = validated_data.pop("description")
        videos = validated_data.pop('video')
        audios = validated_data.pop('audio')
        images = validated_data.pop('image')

        try:
            multimedia, created = Multimedia.objects.get_or_create(
                title=title,
                description=description,
                uploaded_by=user
            )
            if not created:
                raise serializers.ValidationError({
                    "message": "ACCESS DENIED",
                    "detail": "Multimedia already exists.",
                    "status": status.HTTP_403_FORBIDDEN
                })
        except IntegrityError as e:
            raise serializers.ValidationError({
                "detail": e
            })

        for video in videos:
            MultimediaVideo.objects.create(
                video=video,
                multimedia=multimedia,
                **validated_data
            )
        for audio in audios:
            MultimediaAudio.objects.create(
                audio=audio,
                multimedia=multimedia,
                **validated_data
            )
        for image in images:
            MultimediaImage.objects.create(
                image=image,
                multimedia=multimedia,
                **validated_data
            )
        return MultimediaWithMultimediaListSerializer(**validated_data)
