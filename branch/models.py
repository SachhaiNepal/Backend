import os
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


def upload_branch_image_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    branch_name = instance.branch.name.replace(" ", "")
    return f"branch/{branch_name}/images/{filename}"


class Branch(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slogan = models.TextField(max_length=512)
    country = models.ForeignKey(
        "location.Country",
        on_delete=models.DO_NOTHING,
        related_name="branches",
        null=True,
        blank=True,
    )
    province = models.ForeignKey(
        "location.Province",
        on_delete=models.DO_NOTHING,
        related_name="branches",
        null=True,
        blank=True,
    )
    district = models.ForeignKey(
        "location.District",
        on_delete=models.DO_NOTHING,
        related_name="branches",
        null=True,
        blank=True,
    )
    municipality = models.ForeignKey(
        "location.Municipality",
        on_delete=models.DO_NOTHING,
        related_name="branches",
        null=True,
        blank=True,
    )
    municipality_ward = models.OneToOneField(
        "location.MunicipalityWard",
        on_delete=models.DO_NOTHING,
        related_name="branches",
        null=True,
        blank=True,
    )
    vdc = models.ForeignKey(
        "location.VDC",
        on_delete=models.DO_NOTHING,
        related_name="branches",
        null=True,
        blank=True,
    )
    vdc_ward = models.OneToOneField(
        "location.VDCWard",
        on_delete=models.DO_NOTHING,
        related_name="branches",
        null=True,
        blank=True,
    )
    contact = PhoneNumberField(unique=True)
    is_main = models.BooleanField(
        default=False,
        editable=False,
        verbose_name="Is Main Branch"
    )
    is_approved = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="my_approved_branches",
        null=True,
        blank=True,
        editable=False,
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False
    )
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="my_branches",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="my_updated_branches",
        null=True,
        blank=True,
        editable=False,
    )
    timestamp = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Require only vdc or municipality fields
        """
        if not (self.vdc or self.municipality):
            raise ValidationError(
                "One of the location field (municipality | vdc) must be selected."
            )
        elif self.vdc and self.municipality:
            raise ValidationError(
                "Both municipality and vdc fields cannot be selected."
            )
        elif not (self.vdc_ward or self.municipality_ward):
            raise ValidationError(
                "One of the location field (municipality | vdc) ward must be selected."
            )
        elif self.municipality and self.vdc_ward:
            raise ValidationError("Cannot assign vdc ward for a municipality.")
        elif self.vdc_ward and self.municipality_ward:
            raise ValidationError(
                "Both municipality and vdc ward fields cannot be selected."
            )
        elif self.vdc and self.municipality_ward:
            raise ValidationError("Cannot assign municipality ward for a vdc.")

    class Meta:
        ordering = ["-timestamp"]
        verbose_name_plural = "Branches"
        permissions = [
            ("approve_branch", "Can toggle approval status of branch"),
        ]

    def __str__(self):
        return self.name


class BranchImage(models.Model):
    branch = models.ForeignKey(
        "Branch", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to=upload_branch_image_to,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    timestamp = models.DateTimeField(auto_now=True)

    ordering = "-timestamp"

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)
