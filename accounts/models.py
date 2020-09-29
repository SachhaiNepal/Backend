import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from branch.models import Branch


class Member(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True, max_length=1024)
    image = models.ImageField(
        upload_to="member",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )
    temporary_address = models.CharField(max_length=512)
    permanent_address = models.CharField(max_length=512)
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

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        self.user.delete()
        super().delete(using, keep_parents)


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        verbose_name_plural = "Reset Password Codes"

    def __str__(self):
        return "{} - {}".format(self.user.username, self.code)
