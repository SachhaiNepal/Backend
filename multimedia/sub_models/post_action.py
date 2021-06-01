from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


class Comment(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="article_comments",
        null=True,
        blank=True,
    )
    multimedia = models.ForeignKey(
        "Multimedia",
        on_delete=models.CASCADE,
        related_name="multimedia_comments",
        null=True,
        blank=True,
    )
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_comments",
        editable=False,
    )
    comment = models.TextField()
    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies",
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
        ordering = ["-created_at"]

    def __str__(self):
        return self.comment


class BookmarkMedia(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="bookmarked_articles",
        null=True,
        blank=True,
    )
    multimedia = models.ForeignKey(
        "Multimedia",
        on_delete=models.CASCADE,
        related_name="bookmarked_multimedias",
        null=True,
        blank=True,
    )
    is_bookmarked = models.BooleanField(default=False)
    marker = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="bookmarked_medias",
        editable=False,
    )
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
            self.multimedia.title if self.multimedia else self.article.title,
        )


class PinMedia(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="pinned_articles",
        null=True,
        blank=True,
    )
    multimedia = models.ForeignKey(
        "Multimedia",
        on_delete=models.CASCADE,
        related_name="pinned_multimedias",
        null=True,
        blank=True,
    )
    is_pinned = models.BooleanField(default=False)
    pinner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="pinned_medias",
        editable=False,
    )
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
            self.multimedia.title if self.multimedia else self.article.title,
        )


class Love(models.Model):
    article = models.ForeignKey(
        "Article",
        on_delete=models.CASCADE,
        related_name="loved_articles",
        null=True,
        blank=True,
    )
    multimedia = models.ForeignKey(
        "Multimedia",
        on_delete=models.CASCADE,
        related_name="loved_multimedias",
        null=True,
        blank=True,
    )
    is_loved = models.BooleanField(default=False)
    lover = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="loved_medias",
        editable=False,
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
            self.multimedia.title if self.multimedia else self.article.title,
        )
