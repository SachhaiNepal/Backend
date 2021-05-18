import os
import random

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import (
    ALLOWED_VIDEO_EXTENSIONS, MAX_UPLOAD_VIDEO_SIZE, ALLOWED_AUDIO_EXTENSIONS,
    MAX_UPLOAD_AUDIO_SIZE, ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
)
from multimedia.sub_models.post import Multimedia


def upload_multimedia_video_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"multimedias/videos/{instance.multimedia.pk}/{filename}"


def upload_multimedia_audio_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"multimedias/audios/{instance.multimedia.pk}/{filename}"


def upload_multimedia_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"multimedias/images/{instance.multimedia.pk}/{filename}"

class MultimediaVideoUrls(models.Model):
    multimedia = models.ForeignKey(
        Multimedia, on_delete=models.CASCADE, related_name="video_urls"
    )
    video_url = models.URLField()

    def __str__(self):
        return self.video_url

    class Meta:
        verbose_name = "Multimedia Vide Url"
        verbose_name_plural = "Multimedia Vide Urls"


class MultimediaVideo(models.Model):
    video = models.FileField(
        upload_to=upload_multimedia_video_to,
        validators=[FileExtensionValidator(ALLOWED_VIDEO_EXTENSIONS)],
        unique=True,
        verbose_name="Multimedia Video File",
    )
    multimedia = models.ForeignKey(
        Multimedia, on_delete=models.CASCADE, related_name="multimedia_video"
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
        verbose_name = "Multimedia Video"
        verbose_name_plural = "Multimedia Videos"


class MultimediaAudio(models.Model):
    audio = models.FileField(
        upload_to=upload_multimedia_audio_to,
        validators=[FileExtensionValidator(ALLOWED_AUDIO_EXTENSIONS)],
        unique=True,
        verbose_name="Multimedia Audio File",
    )
    multimedia = models.ForeignKey(
        Multimedia, on_delete=models.CASCADE, related_name="multimedia_audio"
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
        verbose_name = "Multimedia Audio"
        verbose_name_plural = "Multimedia Audios"


class MultimediaImage(models.Model):
    image = models.ImageField(
        upload_to=upload_multimedia_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    multimedia = models.ForeignKey(
        Multimedia, on_delete=models.CASCADE, related_name="multimedia_image"
    )

    class Meta:
        verbose_name = "Multimedia Image"
        verbose_name_plural = "Multimedia Images"

    def __str__(self):
        return "{} {}".format(self.multimedia.title, self.image.name)

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)
