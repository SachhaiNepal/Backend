from rest_framework import serializers

from article.models import Article
from utils.file import check_images_size_with_ext


class ArticleWithImageListSerializer(serializers.Serializer):
    """
    create serializer
    creates a new article with image list
    """

    title = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=True, max_length=10000)
    image = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False)
    )

    @staticmethod
    def validate_title(title):
        try:
            Article.objects.get(title=title)
            raise serializers.ValidationError("Article title must be unique.")
        except Article.DoesNotExist:
            return title

    @staticmethod
    def validate_image(obj):
        check_images_size_with_ext(obj)
        return obj
