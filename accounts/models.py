from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from branch.models import Branch
from utils.choices import COUNTRY_CHOICES, DISTRICT_CHOICES


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=512, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, null=True, blank=True)
    district = models.CharField(max_length=14, choices=DISTRICT_CHOICES, null=True)
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
