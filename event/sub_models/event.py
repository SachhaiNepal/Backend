import os
import random

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from utils.constants import EVENT_TYPE, TIME_OF_DAY


def upload_event_banner_to(instance, filename):
    _, file_extension = os.path.splitext(filename)
    filename = str(random.getrandbits(64)) + file_extension
    event_name = instance.event.title.replace(" ", "")
    return f"events/{event_name}/banner/{filename}"


class Event(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField(max_length=512, unique=True)
    venue = models.CharField(max_length=64)
    start_date = models.DateField()
    duration = models.IntegerField()
    time_of_day = models.CharField(max_length=10, choices=TIME_OF_DAY)
    type = models.CharField(max_length=15, choices=EVENT_TYPE)
    is_approved = models.BooleanField(default=False, editable=False)
    is_main = models.BooleanField(default=False, editable=False)
    country = models.ForeignKey(
        "location.Country", on_delete=models.DO_NOTHING, related_name="country_events"
    )
    province = models.ForeignKey(
        "location.Province", on_delete=models.DO_NOTHING, related_name="province_events"
    )
    district = models.ForeignKey(
        "location.District", on_delete=models.DO_NOTHING, related_name="district_events"
    )
    municipality = models.ForeignKey(
        "location.Municipality",
        on_delete=models.DO_NOTHING,
        related_name="municipality_events",
        null=True,
        blank=True,
    )
    municipality_ward = models.ForeignKey(
        "location.MunicipalityWard",
        on_delete=models.DO_NOTHING,
        related_name="municipality_ward_events",
        null=True,
        blank=True,
    )
    vdc = models.ForeignKey(
        "location.VDC",
        on_delete=models.DO_NOTHING,
        related_name="vdc_events",
        null=True,
        blank=True,
    )
    vdc_ward = models.ForeignKey(
        "location.VDCWard",
        on_delete=models.DO_NOTHING,
        related_name="vdc_ward_events",
        null=True,
        blank=True,
    )
    contact = PhoneNumberField()
    branch = models.ForeignKey(
        "branch.Branch",
        on_delete=models.CASCADE,
        related_name="branch_events",
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    approved_at = models.DateTimeField(null=True, blank=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="my_events",
        null=True,
        blank=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="events_updated",
        null=True,
        blank=True,
        editable=False,
    )
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="events_approved",
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        permissions = [
            ("approve_event", "Can toggle approval status of event"),
        ]
        ordering = ("-created_at",)

    def clean(self):
        """
        Require only vdc or municipality
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

    def __str__(self):
        return self.title


class EventBannerImage(models.Model):
    event = models.OneToOneField(
        "Event", on_delete=models.CASCADE, related_name="banner_images"
    )
    image = models.ImageField(
        upload_to=upload_event_banner_to,
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
