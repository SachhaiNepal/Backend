from rest_framework import serializers

from accounts.serializers.user import UserWithProfileSerializer
from multimedia.models import (Multimedia,
                               MultimediaAudio, MultimediaImage,
                               MultimediaVideo, MultimediaVideoUrls)


class MultimediaVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaVideo
        fields = "__all__"


class MultimediaAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaAudio
        fields = "__all__"


class MultimediaVideoUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultimediaVideoUrls
        fields = "__all__"


class MultimediaImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = MultimediaImage
        fields = "__all__"


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
    multimedia_images = MultimediaImageSerializer(many=True, read_only=True)
    multimedia_videos = MultimediaVideoSerializer(many=True, read_only=True)
    multimedia_video_urls = MultimediaVideoUrlsSerializer(many=True, read_only=True)
    multimedia_audios = MultimediaAudioSerializer(many=True, read_only=True)

    uploaded_by = UserWithProfileSerializer()

    class Meta:
        model = Multimedia
        fields = "__all__"
        depth = 1

