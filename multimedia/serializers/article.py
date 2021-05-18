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


class ArticleSerializer(serializers.ModelSerializer):
    uploaded_by = UserWithProfileSerializer()
    approved_at = serializers.SerializerMethodField()
    uploaded_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    @staticmethod
    def get_approved_at(obj):
        return (
            obj.approved_at.strftime("%d %B %Y, %I:%M %p") if obj.approved_at else None
        )

    @staticmethod
    def get_uploaded_at(obj):
        return (
            obj.uploaded_at.strftime("%d %B %Y, %I:%M %p") if obj.uploaded_at else None
        )

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at.strftime("%d %B %Y, %I:%M %p") if obj.updated_at else None

    class Meta:
        model = Article
        fields = "__all__"
        depth = 1


class ArticleImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ArticleImage
        fields = ["image", "article"]


class ArticleImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        exclude = ["article"]
