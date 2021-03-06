import os
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


def upload_profile_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"users/{instance.profile.user.username}/profile_images/{filename}"


def upload_cover_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    return f"users/{instance.profile.user.username}/cover_images/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, editable=False
    )
    bio = models.TextField(null=True, blank=True, max_length=1024)
    contact = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        help_text="Should be a registered Nepal phone number.",
    )
    birth_date = models.DateField(null=True, blank=True)
    current_city = models.CharField(max_length=64, blank=True, null=True)
    home_town = models.CharField(max_length=64, blank=True, null=True)
    country = models.ForeignKey(
        "location.Country",
        on_delete=models.DO_NOTHING,
        related_name="country_followers",
        blank=True,
        null=True,
    )
    province = models.ForeignKey(
        "location.Province",
        on_delete=models.DO_NOTHING,
        related_name="province_followers",
        blank=True,
        null=True,
    )
    district = models.ForeignKey(
        "location.District",
        on_delete=models.DO_NOTHING,
        related_name="district_followers",
        blank=True,
        null=True,
    )
    municipality = models.ForeignKey(
        "location.Municipality",
        on_delete=models.DO_NOTHING,
        related_name="followers",
        null=True,
        blank=True,
    )
    municipality_ward = models.ForeignKey(
        "location.MunicipalityWard",
        on_delete=models.DO_NOTHING,
        related_name="followers",
        null=True,
        blank=True,
    )
    vdc = models.ForeignKey(
        "location.VDC",
        on_delete=models.DO_NOTHING,
        related_name="followers",
        null=True,
        blank=True,
    )
    vdc_ward = models.OneToOneField(
        "location.VDCWard",
        on_delete=models.DO_NOTHING,
        related_name="followers",
        null=True,
        blank=True,
    )
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username + " Profile"

    def clean(self):
        """
        Require only vdc or municipality fields
        """
        if (self.vdc and self.municipality) or (
            self.vdc_ward and self.municipality_ward
        ):
            raise ValidationError(
                "Both municipality and vdc fields cannot be selected."
            )
        elif self.municipality and self.vdc_ward:
            raise ValidationError("Cannot assign vdc ward for a municipality.")
        elif self.vdc and self.municipality_ward:
            raise ValidationError("Cannot assign municipality ward for a vdc.")

    class Meta:
        verbose_name = "Follower Profile"
        verbose_name_plural = "Follower Profiles"


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ProfileImage(models.Model):
    active = models.BooleanField(default=False, editable=False)
    image = models.ImageField(
        upload_to=upload_profile_image_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="profile_images"
    )

    class Meta:
        verbose_name = "Follower Profile Image"
        verbose_name_plural = "Follower Profile Images"

    def __str__(self):
        return self.profile.user.username

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class CoverImage(models.Model):
    active = models.BooleanField(default=False, editable=False)
    image = models.ImageField(
        upload_to=upload_cover_image_to,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="cover_images"
    )

    class Meta:
        verbose_name = "Follower Cover Image"
        verbose_name_plural = "Follower Cover Images"

    def __str__(self):
        return self.profile.user.username

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)
