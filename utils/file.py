from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE, MAX_UPLOAD_AUDIO_SIZE, MAX_UPLOAD_VIDEO_SIZE


def check_size(resources, MAX_SIZE):
    for resource in resources:
        if resource.size / 1000 > MAX_SIZE:
            raise serializers.ValidationError({
                "detail": "Resource {} exceeds maximum upload size.".format(resource.name)
            })


def check_image_size(images):
    check_size(images, MAX_UPLOAD_IMAGE_SIZE)


def check_audio_size(audios):
    check_size(audios, MAX_UPLOAD_AUDIO_SIZE)


def check_video_size(videos):
    check_size(videos, MAX_UPLOAD_VIDEO_SIZE)
