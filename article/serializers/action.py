from rest_framework import serializers

from article.serializers.article import ArticleSerializer
from article.sub_models.action import Bookmark, Comment, Love


class LoveThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Love
        fields = "__all__"


class LoveSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = Love
        fields = "__all__"
        depth = 1


class BookmarkThinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = "__all__"


class BookmarkSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = Bookmark
        fields = "__all__"
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%d %B %Y, %I:%M %p") if obj.created_at else None

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
