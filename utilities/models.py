import os
import random

from django.db import models
from rest_framework.exceptions import ValidationError

from backend.settings import MAX_UPLOAD_IMAGE_SIZE


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
    return f"utilities/services/{filename}"


def upload_about_us_images_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"utilities/about-us/{filename}"


class ShowcaseSlider(models.Model):
    image = models.ImageField(upload_to=upload_showcase_slider_image_to)
    title = models.TextField(max_length=512, null=True, blank=True)
    context = models.TextField(max_length=512, null=True, blank=True)
    subtitle = models.TextField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Showcase Slider"
        verbose_name_plural = "Showcase Slider"

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class ShowcaseGallery(models.Model):
    image = models.ImageField(upload_to=upload_showcase_gallery_image_to)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Showcase Gallery"
        verbose_name_plural = "Showcase Gallery"

    def __str__(self):
        return self.image.name

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class Service(models.Model):
    image = models.ImageField(upload_to=upload_services_images_to)
    title = models.CharField(max_length=16)
    description = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Services"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class AboutUs(models.Model):
    about_us = models.TextField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "About Us"

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"


class AboutUsImage(models.Model):
    image = models.ImageField(upload_to=upload_about_us_images_to)
    about_us = models.ForeignKey(
        AboutUs, on_delete=models.CASCADE, related_name="about_us_images"
    )

    def __str__(self):
        return self.image.name

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)
