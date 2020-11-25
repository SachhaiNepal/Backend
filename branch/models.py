from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


class Branch(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slogan = models.TextField(blank=True, null=True, max_length=512)
    image = models.ImageField(
        upload_to="branch",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )
    country = models.ForeignKey(
        "location.Country",
        on_delete=models.DO_NOTHING,
        related_name="BranchCountry"
    )
    province = models.ForeignKey(
        "location.Province",
        on_delete=models.DO_NOTHING,
        related_name="BranchProvince"
    )
    district = models.ForeignKey(
        "location.District",
        on_delete=models.DO_NOTHING,
        related_name="BranchDistrict"
    )
    municipality = models.ForeignKey(
        "location.Municipality",
        on_delete=models.DO_NOTHING,
        related_name="BranchMunicipality",
        null=True,
        blank=True
    )
    municipality_ward = models.OneToOneField(
        "location.MunicipalityWard",
        on_delete=models.DO_NOTHING,
        related_name="BranchMunicipalityWardNumber",
        null=True,
        blank=True,
    )
    vdc = models.ForeignKey(
        "location.VDC",
        on_delete=models.DO_NOTHING,
        related_name="BranchVdc",
        null=True,
        blank=True
    )
    vdc_ward = models.OneToOneField(
        "location.VDCWard",
        on_delete=models.DO_NOTHING,
        related_name="BranchVdcWardNumber",
        null=True,
        blank=True,
    )
    contacts = ArrayField(models.PositiveBigIntegerField(unique=True), size=3)
    is_main = models.BooleanField(default=False, verbose_name="Is Main Branch")
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="BranchApprover",
        null=True,
        blank=True,
        editable=False
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="Creator",
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="Modifier",
        null=True,
        blank=True,
        editable=False
    )
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Require only vdc or municipality
        """
        if not (self.vdc or self.municipality):
            raise ValidationError("One of the location field (municipality | vdc) must be selected.")
        elif self.vdc and self.municipality:
            raise ValidationError("Both municipality and vdc fields cannot be selected.")
        elif not (self.vdc_ward or self.municipality_ward):
            raise ValidationError("One of the location field (municipality | vdc) ward must be selected.")
        elif self.municipality and self.vdc_ward:
            raise ValidationError("Cannot assign vdc ward for a municipality.")
        elif self.vdc_ward and self.municipality_ward:
            raise ValidationError("Both municipality and vdc ward fields cannot be selected.")
        elif self.vdc and self.municipality_ward:
            raise ValidationError("Cannot assign municipality ward for a vdc.")
        elif self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name

    # delete image if replaced while update
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk:
            this_record = Branch.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        super(Branch, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)
