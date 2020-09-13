from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class Media(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True, unique=True)

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
        unique=True,
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
        unique=True,
        verbose_name="Multimedia Audio File"
    )
    multimedia = models.ForeignKey(
        Multimedia,
        on_delete=models.CASCADE,
        related_name="MultimediaAudio"
    )

    def __str__(self):
        return self.multimedia.title


class MultimediaImage(models.Model):
    image = models.ImageField(
        upload_to="multimedia/images"
    )
    multimedia = models.ForeignKey(
        Multimedia,
        on_delete=models.CASCADE,
        related_name="MultimediaImage"
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


class Comment(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="ArticleComment",
        null=True,
        blank=True,
    )
    multimedia = models.ForeignKey(
        "Multimedia",
        on_delete=models.CASCADE,
        related_name="MultimediaComment",
        null=True,
        blank=True,
    )
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="CommentWriter",
        editable=False
    )
    comment = models.TextField()
    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="CommentReplies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Require article or multimedia
        """
        if not (self.article or self.multimedia):
            raise ValidationError("One of the media must be selected.")
        if self.article and self.multimedia:
            raise ValidationError("Both media cannot be selected.")

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.comment


class Love(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="LoveArticle",
        null=True,
        blank=True,
    )
    multimedia = models.ForeignKey(
        "Multimedia",
        on_delete=models.CASCADE,
        related_name="LoveMultimedia",
        null=True,
        blank=True,
    )
    is_loved = models.BooleanField(default=False)
    lover = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="MediaLover",
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Require article or multimedia
        """
        if not (self.article or self.multimedia):
            raise ValidationError("One of the media must be selected.")
        if self.article and self.multimedia:
            raise ValidationError("Both media cannot be selected.")

    class Meta:
        unique_together = [["article", "lover"], ["multimedia", "lover"]]

    def __str__(self):
        return '"{}" {} "{}"'.format(
            self.lover,
            "loves" if self.is_loved else "does not love",
            self.multimedia.title if self.multimedia else self.article.title
        )
