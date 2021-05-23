from rest_framework import serializers
from multimedia.models import Article, ArticleImage
from accounts.serializers.user import UserWithProfileSerializer


class ArticlePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ("is_approved",)

    def create(self, validated_data):
        validated_data["uploaded_by"] = self.context["request"].user
        branch = Article.objects.create(**validated_data)
        return branch


class ArticleImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ArticleImage
        fields = ["image", "article"]


class ArticleImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        exclude = ["article"]


class ArticleSerializer(serializers.ModelSerializer):
    article_images = ArticleImageSerializer(many=True, read_only=True)
    uploaded_by = UserWithProfileSerializer()

    class Meta:
        model = Article
        fields = "__all__"
        depth = 1
