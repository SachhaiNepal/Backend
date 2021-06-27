import os
import random

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from backend.settings import MAX_UPLOAD_IMAGE_SIZE, ALLOWED_VIDEO_EXTENSIONS, ALLOWED_IMAGES_EXTENSIONS


def validate_only_number_of_instances(obj, count):
    model = obj.__class__
    if model.objects.count() >= count:
        raise ValidationError("Can only create {} {} instance".format(model.name, count))


def upload_feedback_file_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"utilities/feedbacks/{instance.feedback.writer.username}/{filename}"


def upload_showcase_slider_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"utilities/showcase-slider/{filename}"


def upload_showcase_gallery_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"utilities/showcase-gallery/{filename}"


def upload_services_images_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"utilities/services/{instance.service.title}/{filename}"


def upload_about_us_images_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"utilities/about-us/{filename}"


class SliderImage(models.Model):
    image = models.ImageField(upload_to=upload_showcase_slider_image_to)
    title = models.TextField(max_length=512, null=True, blank=True)
    context = models.TextField(max_length=512, null=True, blank=True)
    subtitle = models.TextField(max_length=1024, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Showcase Slider"
        verbose_name_plural = "Showcase Slider"

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")
        validate_only_number_of_instances(self, 1)

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class ShowcaseGalleryImage(models.Model):
    heading = models.CharField(max_length=64, null=True, blank=True)
    content = models.CharField(max_length=512, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=upload_showcase_gallery_image_to)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Showcase Gallery"
        verbose_name_plural = "Showcase Gallery"

    def __str__(self):
        return self.image.name

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")
        validate_only_number_of_instances(self, 15)

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class Service(models.Model):
    title = models.CharField(max_length=16, unique=True)
    description = models.TextField(max_length=1024, unique=True)
    video_url = models.URLField(unique=True, null=True, blank=True)
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_services",
        editable=False
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Services"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=upload_services_images_to)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class AboutUs(models.Model):
    about_us = models.TextField(max_length=10000)
    video_url = models.URLField(unique=True, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "About Us"

    def clean(self):
        validate_only_number_of_instances(self, 1)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"


class AboutUsImage(models.Model):
    image = models.ImageField(upload_to=upload_about_us_images_to)
    about_us = models.ForeignKey(
        AboutUs, on_delete=models.CASCADE, related_name="images"
    )
    content = models.CharField(max_length=1024, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "About Us Image"
        verbose_name_plural = "About Us Images"

    def __str__(self):
        return self.image.name

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class Feedback(models.Model):
    subject = models.CharField(max_length=244, unique=True)
    message = models.TextField(max_length=1024, unique=True)
    writer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="my_feedbacks",
        editable=False
    )
    seen = models.BooleanField(default=False, editable=False)
    reply_to = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replies",
        null=True,
        blank=True
    )
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return self.subject


class FeedbackFile(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(
        validators=[FileExtensionValidator(
            ALLOWED_VIDEO_EXTENSIONS + ALLOWED_IMAGES_EXTENSIONS + ["pdf", "docx", "txt", "zip"]
        )],
        upload_to=upload_feedback_file_to,
        unique=True,
        help_text="File to upload with feedback. Can be image, video, pdf, documents or zip files."
    )
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.feedback.subject}: {self.file.name}"

    def delete(self, using=None, keep_parents=False):
        self.file.delete()
        super().delete(using, keep_parents)
