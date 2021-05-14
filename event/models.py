from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE

TIME_OF_DAY = (
    ("Morning", "Morning"),
    ("Afternoon", "Afternoon"),
    ("Evening", "Evening"),
)

EVENT_TYPE = (
    ("Satsang", "Satsang"),
    ("General Meeting", "General Meeting"),
    ("Board Meeting", "Board Meeting"),
)


class Event(models.Model):
    title = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True, max_length=512)
    venue = models.CharField(max_length=64)
    start_date = models.DateField()
    duration = models.IntegerField()
    time_of_day = models.CharField(max_length=10, choices=TIME_OF_DAY)
    type = models.CharField(max_length=15, choices=EVENT_TYPE)
    is_approved = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    banner = models.ImageField(
        upload_to="events",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    country = models.ForeignKey(
        "location.Country", on_delete=models.DO_NOTHING, related_name="EventCountry"
    )
    province = models.ForeignKey(
        "location.Province", on_delete=models.DO_NOTHING, related_name="EventProvince"
    )
    district = models.ForeignKey(
        "location.District", on_delete=models.DO_NOTHING, related_name="EventDistrict"
    )
    municipality = models.ForeignKey(
        "location.Municipality",
        on_delete=models.DO_NOTHING,
        related_name="EventMunicipality",
        null=True,
        blank=True,
    )
    municipality_ward = models.ForeignKey(
        "location.MunicipalityWard",
        on_delete=models.DO_NOTHING,
        related_name="EventMunicipalityWardNumber",
        null=True,
        blank=True,
    )
    vdc = models.ForeignKey(
        "location.VDC",
        on_delete=models.DO_NOTHING,
        related_name="EventVdc",
        null=True,
        blank=True,
    )
    vdc_ward = models.ForeignKey(
        "location.VDCWard",
        on_delete=models.DO_NOTHING,
        related_name="EventVdcWardNumber",
        null=True,
        blank=True,
    )
    contact = PhoneNumberField(unique=True)
    organizer = models.ForeignKey(
        "branch.Branch",
        on_delete=models.CASCADE,
        related_name="EventOrganizer",
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    approved_at = models.DateTimeField(null=True, blank=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="EventCreator",
        null=True,
        blank=True,
        editable=False,
    )
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="EventModifier",
        null=True,
        blank=True,
        editable=False,
    )
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="EventApprover",
        null=True,
        blank=True,
        editable=False,
    )

    class Meta:
        permissions = [
            ("approve_event", "Can toggle approval status of event"),
        ]

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
        elif self.banner and self.banner.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def __str__(self):
        return self.title

    # delete banner if replaced while update
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pk:
            this_record = Event.objects.get(pk=self.pk)
            if this_record.banner != self.banner:
                this_record.banner.delete(save=False)
        super(Event, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.banner:
            self.banner.delete()
        super().delete(using, keep_parents)


class EventPhoto(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="BaseEvent",
    )
    image = models.ImageField(
        upload_to="event/photos",
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
