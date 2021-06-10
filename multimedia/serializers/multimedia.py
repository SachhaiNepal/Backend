from rest_framework import serializers

from accounts.serializers.user import UserWithProfileSerializer
from multimedia.models import Multimedia
from multimedia.serializers.media import (
    ImageSerializer,
    AudioSerializer, VideoSerializer, VideoUrlSerializer
)


class MultimediaPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multimedia
        fields = "__all__"
        read_only_fields = ("is_approved",)

    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
        branch = Multimedia.objects.create(**validated_data)
        return branch


class MultimediaSerializer(serializers.ModelSerializer):
    multimedia_images = ImageSerializer(many=True, read_only=True)
    multimedia_videos = VideoSerializer(many=True, read_only=True)
    multimedia_video_urls = VideoUrlSerializer(many=True, read_only=True)
    multimedia_audios = AudioSerializer(many=True, read_only=True)

    uploaded_by = UserWithProfileSerializer()

    class Meta:
        model = Multimedia
        fields = "__all__"
        depth = 1
