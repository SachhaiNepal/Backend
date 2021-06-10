from django.contrib.auth import get_user_model
from django.db import models


class Comment(models.Model):
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="article_comments"
    )
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_article_comments",
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
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="bookmarked_articles"
    )
    is_bookmarked = models.BooleanField(default=False)
    marker = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_bookmarked_articles",
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = "Media Bookmarks"

    def __str__(self):
        return '"{}" {} "{}"'.format(
            self.marker,
            "bookmarked" if self.is_bookmarked else "removed bookmark from",
            self.article.title,
        )


class Love(models.Model):
    article = models.ForeignKey(
        "Article", on_delete=models.CASCADE, related_name="loved_articles"
    )
    is_loved = models.BooleanField(default=False)
    lover = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_loved_articles",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '"{}" {} "{}"'.format(
            self.lover,
            "loves" if self.is_loved else "does not love",
            self.article.title,
        )
