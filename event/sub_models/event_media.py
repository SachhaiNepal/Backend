import os
import random

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import (
    ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE, MAX_UPLOAD_VIDEO_SIZE,
    ALLOWED_VIDEO_EXTENSIONS
)
from event.sub_models.event import Event


def upload_event_video_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"events/{instance.event.pk}/video/{filename}"


def upload_event_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"events/{instance.event.pk}/image/{filename}"


class EventVideo(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_videos",
    )
    video = models.FileField(
        upload_to=upload_event_video_to,
        validators=[FileExtensionValidator(ALLOWED_VIDEO_EXTENSIONS)],
    )

    def __str__(self):
        return "{} - {}".format(self.event.title, self.image.name)

    def clean(self):
        if self.video.size / 1000 > MAX_UPLOAD_VIDEO_SIZE:
            raise ValidationError("Video size exceeds max video upload size.")

    def delete(self, using=None, keep_parents=False):
        self.video.delete()
        super().delete(using, keep_parents)


class EventPhoto(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to=upload_event_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )

    def __str__(self):
        return "{} - {}".format(self.event.title, self.image.name)

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)


class EventVideoUrls(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="video_urls"
    )
    video_url = models.URLField(unique=True)

    def __str__(self):
        return self.video_url
