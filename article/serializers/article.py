from rest_framework import serializers

from accounts.serializers.user import UserWithProfileSerializer
from article.models import Article, ArticleImage


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("is_approved",)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        article = Article.objects.create(**validated_data)
        return article


class ArticleImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ArticleImage
        fields = ["id", "image", "article"]


class ArticleImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        exclude = ["article"]


class ArticleSerializer(serializers.ModelSerializer):
    images = ArticleImageSerializer(many=True, read_only=True)
    created_by = UserWithProfileSerializer()

    class Meta:
        model = Article
        fields = "__all__"
        depth = 1
