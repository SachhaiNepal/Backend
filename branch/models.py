from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from utils.choices import COUNTRIES, DISTRICTS


class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=512, unique=True)
    country = models.ForeignKey(
        "accounts.Country",
        on_delete=models.DO_NOTHING,
        related_name="BranchCountry"
    )
    province = models.ForeignKey(
        "accounts.Province",
        on_delete=models.DO_NOTHING,
        related_name="BranchProvince"
    )
    district = models.ForeignKey(
        "accounts.District",
        on_delete=models.DO_NOTHING,
        related_name="BranchDistrict"
    )
    phone = PhoneNumberField(unique=True, max_length=15)

    is_main = models.BooleanField(default=False, verbose_name="Is Main Branch")

    created_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="Creator"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="Modifier",
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
