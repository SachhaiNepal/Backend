from rest_framework import serializers

from multimedia.models import Bookmark, Comment, Love
from multimedia.serializers.multimedia import MultimediaSerializer


class LoveThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Love
        fields = "__all__"


class LoveSerializer(serializers.ModelSerializer):
    multimedia = MultimediaSerializer()

    class Meta:
        model = Love
        fields = "__all__"
        depth = 1


class BookmarkThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"


class BookmarkSerializer(serializers.ModelSerializer):
    multimedia = MultimediaSerializer()

    class Meta:
        model = Bookmark
        fields = "__all__"
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["multimedia", "reply_to"]
        depth = 1


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["writer"] = self.context["request"].user
        return super().create(validated_data)
