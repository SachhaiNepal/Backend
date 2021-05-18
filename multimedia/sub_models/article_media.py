import os
import random

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


def upload_article_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"articles/{instance.article.pk}/{filename}"


class ArticleImage(models.Model):
    image = models.ImageField(
        upload_to=upload_article_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    article = models.ForeignKey(
        "Article", related_name="article_images", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Article Image"
        verbose_name_plural = "Article Images"

    def __str__(self):
        return "{} {}".format(self.article.title, self.image.name)

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)
