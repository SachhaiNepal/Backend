import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from branch.models import Branch


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, editable=False)
    bio = models.TextField(null=True, blank=True, max_length=1024)
    contacts = ArrayField(models.PositiveBigIntegerField(unique=True), size=3, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    current_city = models.CharField(max_length=512, blank=True, null=True)
    home_town = models.CharField(max_length=512, blank=True, null=True)
    country = models.ForeignKey(
        "location.Country",
        on_delete=models.DO_NOTHING,
        related_name="MemberCountry",
        blank=True, null=True
    )
    province = models.ForeignKey(
        "location.Province",
        on_delete=models.DO_NOTHING,
        related_name="MemberProvince",
        blank=True, null=True
    )
    district = models.ForeignKey(
        "location.District",
        on_delete=models.DO_NOTHING,
        related_name="MemberDistrict",
        blank=True, null=True
    )
    last_updated = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return self.user.username + ' Profile'


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ProfileImage(models.Model):
    image = models.ImageField(
        upload_to="follower/profile",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)]
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="FollowerProfileImage"
    )

    def __str__(self):
        return self.profile.user.username

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        self.user.delete()
        super().delete(using, keep_parents)


class Member(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, editable=False)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.DO_NOTHING,
        related_name="Branch",
    )
    is_approved = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="Approver",
        editable=False
    )
    approved_at = models.DateTimeField(default=None, null=True, blank=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="MemberCreator",
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="MemberModifier",
        editable=False
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = "Members"

    def __str__(self):
        return self.user.username


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        verbose_name_plural = "Reset Password Codes"

    def __str__(self):
        return "{} - {}".format(self.user.username, self.code)
