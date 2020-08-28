from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Media(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    approved_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="MultimediaApprover",
        null=True,
        blank=True,
        editable=False
    )
    approved_at = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        editable=False
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="MediaUploader",
        editable=False
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)


class Multimedia(Media):
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class MultimediaVideo(models.Model):
    video = models.FileField(
        upload_to="multimedia/videos",
        validators=[FileExtensionValidator(["webm", "mp4", "mpeg", "flv"])],
        verbose_name="Multimedia Video File"
    )
    multimedia = models.ForeignKey(
        Multimedia,
        on_delete=models.CASCADE,
        related_name="MultimediaVideo"
    )

    def __str__(self):
        return self.multimedia.title


class MultimediaAudio(models.Model):
    audio = models.FileField(
        upload_to="multimedia/audios",
        validators=[FileExtensionValidator(["mp3", "wav"])],
        blank=True,
        null=True,
        verbose_name="Multimedia Audio File"
    )
    multimedia = models.ForeignKey(
        Multimedia,
        on_delete=models.CASCADE,
        related_name="MultimediaAudio"
    )

    def __str__(self):
        return self.multimedia.title


class Article(Media):
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    image = models.ImageField(
        upload_to="articles"
    )
    article = models.ForeignKey(
        "Article",
        related_name="ArticleImage",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.article.title
