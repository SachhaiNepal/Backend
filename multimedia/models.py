from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import (ALLOWED_AUDIO_EXTENSIONS,
                              ALLOWED_IMAGES_EXTENSIONS,
                              ALLOWED_VIDEO_EXTENSIONS, MAX_UPLOAD_AUDIO_SIZE,
                              MAX_UPLOAD_IMAGE_SIZE, MAX_UPLOAD_VIDEO_SIZE)


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
        validators=[FileExtensionValidator(ALLOWED_VIDEO_EXTENSIONS)],
        unique=True,
        verbose_name="Multimedia Video File"
    )
    multimedia = models.ForeignKey(
        Multimedia,
        on_delete=models.CASCADE,
        related_name="MultimediaVideo"
    )

    def __str__(self):
        return "{} {}".format(self.multimedia.title, self.video.name)

    def clean(self):
        if self.video.size / 1000 > MAX_UPLOAD_VIDEO_SIZE:
            raise ValidationError("Video size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.video.delete()
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Multimedia Videos"


class MultimediaAudio(models.Model):
    audio = models.FileField(
        upload_to="multimedia/audios",
        validators=[FileExtensionValidator(ALLOWED_AUDIO_EXTENSIONS)],
        unique=True,
        verbose_name="Multimedia Audio File"
    )
    multimedia = models.ForeignKey(
        Multimedia,
        on_delete=models.CASCADE,
        related_name="MultimediaAudio"
    )

    def __str__(self):
        return "{} {}".format(self.multimedia.title, self.audio.name)

    def clean(self):
        if self.audio.size / 1000 > MAX_UPLOAD_AUDIO_SIZE:
            raise ValidationError("Audio size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.audio.delete()
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Multimedia Audios"


class MultimediaImage(models.Model):
    image = models.ImageField(
        upload_to="multimedia/images",
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )
    multimedia = models.ForeignKey(
        Multimedia,
        on_delete=models.CASCADE,
        related_name="MultimediaImage"
    )

    class Meta:
        verbose_name = "Multimedia Images"

    def __str__(self):
        return "{} {}".format(self.multimedia.title, self.image.name)

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)


class Article(Media):
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class ArticleImage(models.Model):
    image = models.ImageField(
        upload_to="articles",
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )
    article = models.ForeignKey(
        "Article",
        related_name="ArticleImage",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Article Images"

    def __str__(self):
        return "{} {}".format(self.article.title, self.image.name)

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)


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


class BookmarkMedia(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="BookmarkArticle",
        null=True,
        blank=True,
    )
    multimedia = models.ForeignKey(
        "Multimedia",
        on_delete=models.CASCADE,
        related_name="BookmarkMultimedia",
        null=True,
        blank=True,
    )
    is_bookmarked = models.BooleanField(default=False)
    marker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="BookmarkActor", editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def clean(self):
        """
        Require article or multimedia
        """
        if not (self.article or self.multimedia):
            raise ValidationError("One of the media must be selected.")
        if self.article and self.multimedia:
            raise ValidationError("Both media cannot be selected.")

    class Meta:
        verbose_name_plural = "Media Bookmarks"
        unique_together = [["article", "marker"], ["multimedia", "marker"]]

    def __str__(self):
        return '"{}" {} "{}"'.format(
            self.marker,
            "bookmarked" if self.is_bookmarked else "removed bookmark from",
            self.multimedia.title if self.multimedia else self.article.title
        )


class PinMedia(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="PinArticle",
        null=True,
        blank=True,
    )
    multimedia = models.ForeignKey(
        "Multimedia",
        on_delete=models.CASCADE,
        related_name="PinMultimedia",
        null=True,
        blank=True,
    )
    is_pinned = models.BooleanField(default=False)
    pinner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="BookmarkPinner", editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    def clean(self):
        """
        Require article or multimedia
        """
        if not (self.article or self.multimedia):
            raise ValidationError("One of the media must be selected.")
        if self.article and self.multimedia:
            raise ValidationError("Both media cannot be selected.")

    class Meta:
        verbose_name_plural = "Pinned Medias"
        unique_together = [["article", "pinner"], ["multimedia", "pinner"]]

    def __str__(self):
        return '"{}" {} "{}"'.format(
            self.pinner,
            "pinned" if self.is_pinned else "removed pin from",
            self.multimedia.title if self.multimedia else self.article.title
        )


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
