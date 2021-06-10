from django.contrib.auth import get_user_model
from django.db import models


class Comment(models.Model):
    multimedia = models.ForeignKey(
        "Multimedia", on_delete=models.CASCADE, related_name="comments"
    )
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_comments",
        editable=False,
    )
    comment = models.TextField()
    reply_to = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

    def __str__(self):
        return self.comment


class Bookmark(models.Model):
    multimedia = models.ForeignKey(
        "Multimedia", on_delete=models.CASCADE, related_name="multimedias"
    )
    is_bookmarked = models.BooleanField(default=False)
    marker = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="bookmarked_medias",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = "Media Bookmarks"

    def __str__(self):
        return '"{}" {} "{}"'.format(
            self.marker,
            "bookmarked" if self.is_bookmarked else "removed bookmark from",
            self.multimedia,
        )


class Love(models.Model):
    multimedia = models.ForeignKey(
        "Multimedia", on_delete=models.CASCADE, related_name="loved"
    )
    is_loved = models.BooleanField(default=False)
    lover = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_loves",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '"{}" {} "{}"'.format(
            self.lover,
            "loves" if self.is_loved else "does not love",
            self.multimedia,
        )
