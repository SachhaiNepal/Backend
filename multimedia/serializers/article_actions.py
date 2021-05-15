from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from multimedia.models import (Article, BookmarkMedia, Comment, Love,
                               Multimedia, PinMedia)
from multimedia.serializers.model_serializer import ArticleSerializer, MultimediaSerializer


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
        fields = "__all__"
        depth = 1


class CommentPostSerializer(serializers.ModelSerializer):
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all(), required=False
    )
    multimedia = serializers.PrimaryKeyRelatedField(
        queryset=Multimedia.objects.all(), required=False
    )

    class Meta:
        model = Comment
        fields = ["article", "multimedia", "comment"]

    def validate(self, validated_data):
        if validated_data.get("article") and validated_data.get("multimedia"):
            raise ValidationError("Both media types cannot be selected.")
        elif not validated_data.get("article") and not validated_data.get("multimedia"):
            raise ValidationError("At least a media type should be selected.")
        else:
            return validated_data

    def create(self, validated_data):
        validated_data["writer"] = self.context["request"].user
        return Comment.objects.create(**validated_data)
