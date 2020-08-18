from django.db import models

from utils.choices import COUNTRY_CHOICES, DISTRICT_CHOICES


class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=512, unique=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    district = models.CharField(max_length=14, choices=DISTRICT_CHOICES, unique=True)
    phone = models.BigIntegerField(unique=True)
    is_main = models.BooleanField(default=False, verbose_name="Is Main Branch")

    created_by = models.ForeignKey("accounts.Member", on_delete=models.DO_NOTHING, related_name="Creator")
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey("accounts.Member", on_delete=models.DO_NOTHING, related_name="Modifier", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
