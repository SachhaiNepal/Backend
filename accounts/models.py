import uuid

from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from branch.models import Branch


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    temporary_address = models.CharField(max_length=512, blank=True, null=True)
    permanent_address = models.CharField(max_length=512, blank=True, null=True)
    country = models.ForeignKey(
        "location.Country",
        on_delete=models.DO_NOTHING,
        related_name="MemberCountry"
    )
    province = models.ForeignKey(
        "location.Province",
        on_delete=models.DO_NOTHING,
        related_name="MemberProvince"
    )
    district = models.ForeignKey(
        "location.District",
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
        related_name="Approver",
        editable=False
    )
    approved_at = models.DateTimeField(default=None, null=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = "Members"

    def __str__(self):
        return self.user.username


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        verbose_name_plural = "Reset Password Codes"

    def __str__(self):
        return "{} - {}".format(self.user.username, self.code)
