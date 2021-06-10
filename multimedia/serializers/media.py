from rest_framework import serializers

from multimedia.sub_models.media import Image, Sound, Video, VideoUrl
from utils.helper import get_youtube_video_data


class VideoUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUrl
        fields = "__all__"

    def create(self, validated_data):
        video_url = validated_data.get("video_url")
        yt_info = get_youtube_video_data(video_url)
        validated_data["yt_info"] = yt_info
        return super().create(validated_data)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
