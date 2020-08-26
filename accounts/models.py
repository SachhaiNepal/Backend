from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from branch.models import Branch
from utils.choices import COUNTRIES, DISTRICTS


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=255, unique=True)
    number = models.IntegerField(
        unique=True,
        validators=[
            MaxValueValidator(7),
            MinValueValidator(1)
        ]
    )
    country = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        related_name="RelatedCountryForProvince"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=255, unique=True)
    province = models.ForeignKey(
        "Province",
        on_delete=models.CASCADE,
        related_name="RelatedProvince"
    )
    country = models.ForeignKey(
        "Country",
        on_delete=models.CASCADE,
        related_name="RelatedCountryForDistrict"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    temporary_address = models.CharField(max_length=512, blank=True, null=True)
    permanent_address = models.CharField(max_length=512, blank=True, null=True)
    country = models.ForeignKey(
        "Country",
        on_delete=models.DO_NOTHING,
        related_name="MemberCountry"
    )
    province = models.ForeignKey(
        "Province",
        on_delete=models.DO_NOTHING,
        related_name="MemberProvince"
    )
    district = models.ForeignKey(
        "District",
        on_delete=models.DO_NOTHING,
        related_name="MemberDistrict"
    )

    phone = PhoneNumberField(unique=True, blank=True, null=True)

    branch = models.ForeignKey(
        Branch,
        on_delete=models.DO_NOTHING,
        related_name="Branch",
        null=True,
        blank=True
    )

    is_approved = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="Approver"
    )
    approved_at = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Members"

    def __str__(self):
        return self.user.username
