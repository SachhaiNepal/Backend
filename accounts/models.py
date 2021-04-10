import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from branch.models import Branch
from utils.constants import MEMBER_ROLE_CHOICES


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, editable=False)
    bio = models.TextField(null=True, blank=True, max_length=1024)
    contact = PhoneNumberField(unique=True, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    current_city = models.CharField(max_length=512, blank=True, null=True)
    home_town = models.CharField(max_length=512, blank=True, null=True)
    country = models.ForeignKey(
        "location.Country",
        on_delete=models.DO_NOTHING,
        related_name="country_followers",
        blank=True, null=True
    )
    province = models.ForeignKey(
        "location.Province",
        on_delete=models.DO_NOTHING,
        related_name="province_followers",
        blank=True, null=True
    )
    district = models.ForeignKey(
        "location.District",
        on_delete=models.DO_NOTHING,
        related_name="district_followers",
        blank=True, null=True
    )
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username + ' Profile'

    class Meta:
        verbose_name = "Follower Profile"
        verbose_name_plural = "Follower Profiles"


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
        related_name="follower_profile_images"
    )

    class Meta:
        verbose_name = "Follower Profile Image"
        verbose_name_plural = "Follower Profile Images"

    def __str__(self):
        return self.profile.user.username

    def clean(self):
        if self.image and self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete(using, keep_parents)


class Member(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False, editable=False)
    approved_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="approved_members",
        editable=False
    )
    approved_at = models.DateTimeField(default=None, null=True, blank=True, editable=False)
    created_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="members_created",
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_by = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="members_updated",
        editable=False
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name_plural = "Members"
        permissions = [
            ("approve_member", "Can toggle approval status of member"),
        ]

    def __str__(self):
        return self.user.username


class ResetPasswordCode(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reset_pw_codes")
    code = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        verbose_name_plural = "Reset Password Codes"

    def __str__(self):
        return "{} - {}".format(self.user.username, self.code)


class MemberRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="member_role")
    role_name = models.CharField(max_length=18, choices=MEMBER_ROLE_CHOICES)
    from_date = models.DateField()
    to_date = models.DateField()
    branch = models.PositiveBigIntegerField()

    class Meta:
        verbose_name = "Member Role"
        verbose_name_plural = "Member Roles"
        unique_together = ("member", "role_name", "branch")

    def clean(self):
        selected_member = self.member
        selected_branch = self.branch
        # check if selected branch id is valid
        try:
            Branch.objects.get(pk=selected_branch)
        except Branch.DoesNotExist:
            raise ValidationError("Selected branch does not exist.")
        # check if member is registered in selected branch
        member_branches = MemberBranch.objects.filter(member=selected_member)
        found = False
        for member_branch in member_branches:
            if member_branch.id == selected_branch:
                found = True
        if not found:
            raise ValidationError("Member not registered in selected branch.")

    def __str__(self):
        return self.member.user.username


class MemberBranch(models.Model):
    member = models.ForeignKey(Member, on_delete=models.DO_NOTHING, related_name="member_branches")
    branch = models.PositiveBigIntegerField()
    date_of_membership = models.DateField()

    class Meta:
        verbose_name = "Member Branch"
        verbose_name_plural = "Member Branches"
        unique_together = ("member", "branch")

    def __str__(self):
        return self.member.user.username

    def clean(self):
        selected_branch = self.branch
        # check if selected branch id is valid
        try:
            Branch.objects.get(pk=selected_branch)
        except Branch.DoesNotExist:
            raise ValidationError("Selected branch does not exist.")
