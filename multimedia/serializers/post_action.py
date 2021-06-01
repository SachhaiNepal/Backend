from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from multimedia.models import (Article, BookmarkMedia, Comment, Love,
                               Multimedia, PinMedia)
from multimedia.serializers.article import ArticleSerializer
from multimedia.serializers.multimedia import MultimediaSerializer


class LoveSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    multimedia = MultimediaSerializer()

    class Meta:
        model = Love
        fields = "__all__"
        depth = 1


class BookmarkMediaSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    multimedia = MultimediaSerializer()

    class Meta:
        model = BookmarkMedia
        fields = "__all__"
        depth = 1


class PinMediaSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    multimedia = MultimediaSerializer()

    class Meta:
        model = PinMedia
        fields = "__all__"
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%d %B %Y, %I:%M %p") if obj.created_at else None

    class Meta:
        model = Comment
        exclude = ["article", "multimedia", "reply_to"]
        depth = 1


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def validate(self, validated_data):
        print(validated_data)
        if validated_data.get("article") and validated_data.get("multimedia"):
            raise ValidationError("Both media types cannot be selected.")
        elif not validated_data.get("article") and not validated_data.get("multimedia"):
            raise ValidationError("At least a media type should be selected.")
        else:
            return validated_data

    def create(self, validated_data):
        validated_data["writer"] = self.context["request"].user
        return super().create(validated_data)
