from rest_framework import serializers

from article.models import Article, Image
from article.sub_models.media import CoverImage, ImageUrl
from utils.global_serializer import UserWithActiveProfileMediaSerializer


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("is_approved",)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        article = Article.objects.create(**validated_data)
        return article


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = ["id", "image", "article"]


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ["article"]


class CoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverImage
        exclude = ["article"]


class CoverImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverImage
        fields = "__all__"


class ImageUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUrl
        exclude = ["article"]


class ImageUrlCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUrl
        fields = "__all__"


class ListForMeSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    image_urls = ImageUrlSerializer(many=True, read_only=True)
    cover_images = CoverImageSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        exclude = ["created_by"]
        depth = 1


class ListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    image_urls = ImageUrlSerializer(many=True, read_only=True)
    cover_images = CoverImageSerializer(many=True, read_only=True)
    created_by = UserWithActiveProfileMediaSerializer(allow_null=True)

    class Meta:
        model = Article
        fields = "__all__"
        depth = 1
