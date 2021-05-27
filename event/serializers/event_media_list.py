from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from event.sub_models.event import Event
from event.sub_models.event_media import EventPhoto, EventVideo, EventVideoUrl
from utils.file import check_image_size_with_ext, check_video_size_with_ext


class AddEventImageListSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False)
    )

    def validate_images(self, obj):
        check_image_size_with_ext(obj)
        return obj

    def create(self, validated_data):
        images = validated_data.get("images")
        event_id = self.context.get("event_id")
        event = get_object_or_404(Event, pk=event_id)
        for image in images:
            EventPhoto.objects.create(image=image, event=event)
        return event


class AddEventVideoUrlListSerializer(serializers.Serializer):
    video_urls = serializers.ListField(
        child=serializers.URLField(
            validators=[
                RegexValidator(
                    regex=r"https:\/\/www\.youtube\.com\/*",
                    message="URL must be sourced from youtube.",
                )
            ]
        ),
    )

    def create(self, validated_data):
        video_urls = validated_data.get("video_urls")
        event_id = self.context.get("event_id")
        event = get_object_or_404(Event, pk=event_id)
        for video_url in video_urls:
            EventVideoUrl.objects.create(video_url=video_url, event=event)
        return event


class AddEventVideoListSerializer(serializers.Serializer):
    videos = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        required=False,
    )

    def validate_videos(self, obj):
        check_video_size_with_ext(obj)
        return obj

    def create(self, validated_data):
        videos = validated_data.get("videos")
        event_id = self.context.get("event_id")
        event = get_object_or_404(Event, pk=event_id)
        for video in videos:
            EventVideo.objects.create(video=video, event=event)
        return event
