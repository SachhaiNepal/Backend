import os
import random

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import (ALLOWED_AUDIO_EXTENSIONS,
                              ALLOWED_IMAGES_EXTENSIONS,
                              ALLOWED_VIDEO_EXTENSIONS, MAX_UPLOAD_AUDIO_SIZE,
                              MAX_UPLOAD_IMAGE_SIZE, MAX_UPLOAD_VIDEO_SIZE)
from multimedia.sub_models.multimedia import Multimedia


def upload_video_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"multimedias/{instance.multimedia.pk}/videos/{filename}"


def upload_audio_poster_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"multimedias/{instance.multimedia.pk}/audios/poster/{filename}"


def upload_video_poster_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"multimedias/{instance.multimedia.pk}/videos/poster/{filename}"


def upload_audio_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"multimedias/{instance.multimedia.pk}/audios/{filename}"


def upload_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"multimedias/{instance.multimedia.pk}/images/{filename}"


class VideoUrl(models.Model):
    multimedia = models.ForeignKey(
        Multimedia, on_delete=models.CASCADE, related_name="multimedia_video_urls"
    )
    video_url = models.URLField()
    yt_info = models.JSONField(editable=False, null=True, blank=True)

    def __str__(self):
        return self.video_url

    class Meta:
        verbose_name = "Multimedia Video Url"
        verbose_name_plural = "Multimedia Video Urls"


class Video(models.Model):
    video = models.FileField(
        upload_to=upload_video_to,
        validators=[FileExtensionValidator(ALLOWED_VIDEO_EXTENSIONS)],
        verbose_name="Multimedia Video File",
    )
    title = models.CharField(max_length=64, null=True, blank=True)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ImageField(upload_to=upload_video_poster_to, null=True, blank=True)
    multimedia = models.ForeignKey(
        Multimedia, on_delete=models.CASCADE, related_name="multimedia_videos"
    )

    def __str__(self):
        return "{} {}".format(self.multimedia.title, self.video.name)

    def clean(self):
        if self.video.size / 1000 > MAX_UPLOAD_VIDEO_SIZE:
            raise ValidationError("Video size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.poster:
            self.poster.delete()
        self.video.delete()
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Multimedia Video"
        verbose_name_plural = "Multimedia Videos"


class Sound(models.Model):
    sound = models.FileField(
        upload_to=upload_audio_to,
        validators=[FileExtensionValidator(ALLOWED_AUDIO_EXTENSIONS)],
        verbose_name="Multimedia Audio File",
    )
    title = models.CharField(max_length=64, null=True, blank=True)
    artist = models.CharField(max_length=64, null=True, blank=True)
    poster = models.ImageField(upload_to=upload_audio_poster_to, null=True, blank=True)
    multimedia = models.ForeignKey(
        Multimedia, on_delete=models.CASCADE, related_name="multimedia_sounds"
    )

    def __str__(self):
        return "{} {}".format(self.multimedia.title, self.sound.name)

    def clean(self):
        if self.sound.size / 1000 > MAX_UPLOAD_AUDIO_SIZE:
            raise ValidationError("Audio size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.poster:
            self.poster.delete()
        self.sound.delete()
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = "Multimedia Sound"
        verbose_name_plural = "Multimedia Sounds"


class Image(models.Model):
    image = models.ImageField(
        upload_to=upload_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    multimedia = models.ForeignKey(
        Multimedia, on_delete=models.CASCADE, related_name="multimedia_images"
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
