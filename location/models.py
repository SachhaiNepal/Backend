from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Countries"

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


class Municipality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    district = models.ForeignKey(
        "District",
        on_delete=models.CASCADE,
        related_name="RelatedMunicipalityForDistrict"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Municipalities"

    def __str__(self):
        return self.name


class VDC(models.Model):
    name = models.CharField(max_length=255, unique=True)
    district = models.ForeignKey(
        "District",
        on_delete=models.CASCADE,
        related_name="RelatedVDCForDistrict"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "VDCs"

    def __str__(self):
        return self.name


class VDCWard(models.Model):
    name = models.CharField(max_length=255, unique=True)
    number = models.IntegerField(
        unique=True,
        validators=[
            MaxValueValidator(40),
            MinValueValidator(1)
        ]
    )
    vdc = models.ForeignKey(
        "VDC",
        on_delete=models.CASCADE,
        related_name="RelatedWardForVDC"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "VDC Wards"

    def __str__(self):
        return self.name


class MunicipalityWard(models.Model):
    name = models.CharField(max_length=255, unique=True)
    number = models.IntegerField(
        unique=True,
        validators=[
            MaxValueValidator(40),
            MinValueValidator(1)
        ]
    )
    municipality = models.ForeignKey(
        "Municipality",
        on_delete=models.CASCADE,
        related_name="RelatedWardForMunicipality"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Municipality Wards"

    def __str__(self):
        return self.name
