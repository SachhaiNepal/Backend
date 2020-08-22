from django.core.validators import FileExtensionValidator
from django.db import models


class Multimedia(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video = models.FileField(
        upload_to="multimedia/videos",
        validators=[FileExtensionValidator(['webm', 'mp4', 'mpeg', 'flv'])],
        verbose_name="Multimedia Video File"
    )
    audio = models.FileField(
        upload_to="multimedia/audios",
        validators=[FileExtensionValidator(['mp3', 'wav'])],
        blank=True,
        null=True,
        verbose_name="Multimedia Audio File"
    )

    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        "accounts.Member",
        on_delete=models.DO_NOTHING,
        related_name="MultimediaApprover",
        null=True,
        blank=True
    )
    approved_at = models.DateTimeField(default=None, null=True, blank=True)

    uploaded_by = models.ForeignKey(
        "accounts.Member",
        on_delete=models.DO_NOTHING,
        related_name="MediaUploader"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
