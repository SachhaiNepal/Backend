from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=512, unique=True)
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

    def __str__(self):
        return self.name
