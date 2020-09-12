from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)

    image = models.ImageField(upload_to="branch", null=True, blank=True)

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
        related_name="BranchMunicipalityWardNo",
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
        related_name="BranchVdcWardNo",
        null=True,
        blank=True,
    )

    phone = PhoneNumberField(unique=True, max_length=15)

    is_main = models.BooleanField(default=False, verbose_name="Is Main Branch")

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

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name
