from django.db import IntegrityError
from rest_framework import serializers, status

from multimedia.models import Article, ArticleImage
from utils.file import check_image_size_with_ext
from utils.helper import get_keys_from_ordered_dict


class AddArticleImageListSerializer(serializers.Serializer):
    image = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=True
        ),
        required=True
    )

    def validate_image(self, obj):
        check_image_size_with_ext(obj)
        return obj

    def create(self, validated_data):
        article_id = self.context["article_id"]
        images = validated_data.pop("image")

        article = Article.objects.get(pk=article_id)
        for image in images:
            article, created = ArticleImage.objects.get_or_create(
                image=image,
                article=article,
                **validated_data
            )
        return AddArticleImageListSerializer(**validated_data)


class ArticleWithImageListCreateSerializer(serializers.Serializer):
    image = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=False
        )
    )
    title = serializers.CharField(required=True, max_length=512)
    description = serializers.CharField(required=True, max_length=1024)

    def validate_title(self, title):
        try:
            Article.objects.get(title=title)
            raise serializers.ValidationError("Article title must be unique.")
        except Article.DoesNotExist:
            return title

    def validate_description(self, description):
        try:
            Article.objects.get(description=description)
            raise serializers.ValidationError("Article description must be unique.")
        except Article.DoesNotExist:
            return description

    def validate_image(self, obj):
        check_image_size_with_ext(obj)
        return obj

    def create(self, validated_data):
        keys = get_keys_from_ordered_dict(validated_data)
        user = self.context["request"].user
        title = validated_data.pop("title")
        description = validated_data.pop("description")
        try:
            article, created = Article.objects.get_or_create(
                title=title,
                description=description,
                uploaded_by=user
            )
            if not created:
                raise serializers.ValidationError({
                    "message": "ACCESS DENIED",
                    "detail": "Article already exists.",
                    "status": status.HTTP_400_BAD_REQUEST
                })
        except IntegrityError as e:
            raise serializers.ValidationError({
                "detail": e
            })
        if "image" in keys:
            images = validated_data.pop('image')
            for image in images:
                ArticleImage.objects.create(
                    image=image,
                    article=article,
                    **validated_data
                )
        return ArticleWithImageListCreateSerializer(**validated_data)
