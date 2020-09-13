import re

from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE, MAX_UPLOAD_AUDIO_SIZE, MAX_UPLOAD_VIDEO_SIZE, \
    ALLOWED_IMAGES_EXTENSIONS, ALLOWED_AUDIO_EXTENSIONS, ALLOWED_VIDEO_EXTENSIONS


def check_size(resource, max_size):
    """
    Serializer validator
    Validates file size
    Raises serializer validation error if requirement does not match
    """
    if resource.size / 1000 > max_size:
        raise serializers.ValidationError(
            f"Resource '{resource.name}' exceeds maximum upload size."
            f" Allowed maximum size: {max_size} KB")


def check_extension(resource, allowed_extensions_array):
    """
    Serializer Validator
    Validates file extension
    Raises serializer validation error if requirement does not match
    """
    ext = re.split("\.", resource.name)[1]
    if ext not in allowed_extensions_array:
        raise serializers.ValidationError(
            f"Resource extension '{ext}' is not allowed for upload."
            f" Allowed extensions are: {', '.join(allowed_extensions_array)}"
        )


def check_image_size_with_ext(images):
    for image in images:
        check_extension(image, ALLOWED_IMAGES_EXTENSIONS)
        check_size(image, MAX_UPLOAD_IMAGE_SIZE)


def check_audio_size_with_ext(audios):
    for audio in audios:
        check_extension(audio, ALLOWED_AUDIO_EXTENSIONS)
        check_size(audio, MAX_UPLOAD_AUDIO_SIZE)


def check_video_size_with_ext(videos):
    for video in videos:
        check_extension(video, ALLOWED_VIDEO_EXTENSIONS)
        check_size(video, MAX_UPLOAD_VIDEO_SIZE)
