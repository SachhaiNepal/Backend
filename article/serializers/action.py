from rest_framework import serializers

from article.serializers.article import ListSerializer
from article.sub_models.action import Bookmark, Comment, Love


class LoveThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Love
        fields = "__all__"


class LoveSerializer(serializers.ModelSerializer):
    article = ListSerializer()

    class Meta:
        model = Love
        fields = "__all__"
        depth = 1


class BookmarkThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"


class BookmarkSerializer(serializers.ModelSerializer):
    article = ListSerializer()

    class Meta:
        model = Bookmark
        fields = "__all__"
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["article", "reply_to"]
        depth = 1


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        validated_data["writer"] = self.context["request"].user
        return super().create(validated_data)
