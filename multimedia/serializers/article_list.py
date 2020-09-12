from django.db import IntegrityError
from rest_framework import serializers, status

from multimedia.models import Article, ArticleImage
from utils.file import check_image_size


class ArticleImageListCreateSerializer(serializers.Serializer):
    image = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=True
        ),
        required=True
    )

    def validate(self, data):
        check_image_size(data["image"])
        return data

    def create(self, validated_data):
        article_id = self.context["article_id"]
        images = validated_data.pop("image")

        article = Article.objects.get(pk=article_id)
        print(article)
        for image in images:
            article, created = ArticleImage.objects.get_or_create(
                image=image,
                article=article,
                **validated_data
            )
        return ArticleImageListCreateSerializer(**validated_data)


class ArticleWithImageListSerializer(serializers.Serializer):
    image = serializers.ListField(
        child=serializers.FileField(
            allow_empty_file=False,
            use_url=False
        )
    )
    title = serializers.CharField(required=True, max_length=512)
    description = serializers.CharField(required=True, max_length=1024)

    def validate(self, data):
        check_image_size(data["image"])
        return data

    def create(self, validated_data):
        user = self.context["request"].user
        title = validated_data.pop("title")
        description = validated_data.pop("description")
        images = validated_data.pop('image')

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

        for image in images:
            ArticleImage.objects.create(
                image=image,
                article=article,
                **validated_data
            )
        return ArticleWithImageListSerializer(**validated_data)
