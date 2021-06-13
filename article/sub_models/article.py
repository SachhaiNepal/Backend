from django.contrib.auth import get_user_model
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255, unique=True, null=True)
    description = models.CharField(blank=True, null=True, max_length=10000)
    is_pinned = models.BooleanField(default=False, editable=False)
    pinner = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="pinned_articles",
        null=True,
        blank=True,
        editable=False,
    )
    is_approved = models.BooleanField(default=False, editable=False)
    approved_at = models.DateTimeField(
        default=None, null=True, blank=True, editable=False
    )
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="approved_articles",
        null=True,
        blank=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="my_articles",
        editable=False,
    )
    completed_writing = models.BooleanField(default=False, editable=False)
    timestamp = models.DateTimeField(auto_now=True, editable=False)

    # def __str__(self):
    #     return self.title

    class Meta:
        ordering = ["-timestamp"]
