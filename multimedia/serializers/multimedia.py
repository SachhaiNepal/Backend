from rest_framework import serializers

from multimedia.models import Multimedia
from multimedia.serializers.media import (AudioSerializer, ImageSerializer,
                                          VideoSerializer, VideoUrlSerializer)
from utils.global_serializer import UserWithActiveProfileMediaSerializer


class MultimediaPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multimedia
        fields = "__all__"
        read_only_fields = ("is_approved",)

    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
        branch = Multimedia.objects.create(**validated_data)
        return branch


class ListForMeSerializer(serializers.ModelSerializer):
    multimedia_images = ImageSerializer(many=True, read_only=True)
    multimedia_videos = VideoSerializer(many=True, read_only=True)
    multimedia_video_urls = VideoUrlSerializer(many=True, read_only=True)
    multimedia_audios = AudioSerializer(many=True, read_only=True)

    class Meta:
        model = Multimedia
        exclude = ["uploaded_by"]
        depth = 1


class MultimediaSerializer(serializers.ModelSerializer):
    multimedia_images = ImageSerializer(many=True, read_only=True)
    multimedia_videos = VideoSerializer(many=True, read_only=True)
    multimedia_video_urls = VideoUrlSerializer(many=True, read_only=True)
    multimedia_audios = AudioSerializer(many=True, read_only=True)

    uploaded_by = UserWithActiveProfileMediaSerializer()

    class Meta:
        model = Multimedia
        fields = "__all__"
        depth = 1
