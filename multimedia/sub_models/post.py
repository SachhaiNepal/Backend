from django.contrib.auth import get_user_model
from django.db import models


class Media(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True, unique=True, max_length=512)
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="approved_medias",
        null=True,
        blank=True,
        editable=False,
    )
    approved_at = models.DateTimeField(
        default=None, null=True, blank=True, editable=False
    )
    uploaded_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="uploaded_medias",
        editable=False,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        permissions = [
            ("approve_media", "Can toggle approval status of media"),
        ]


class Multimedia(Media):
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Article(Media):
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
