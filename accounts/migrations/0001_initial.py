# Generated by Django 3.1.8 on 2021-05-23 17:13

import uuid

import django.core.validators
import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models

import accounts.sub_models.profile


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("location", "0001_initial"),
        ("branch", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_approved", models.BooleanField(default=False, editable=False)),
                (
                    "approved_at",
                    models.DateTimeField(
                        blank=True, default=None, editable=False, null=True
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "approved_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="approved_members",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="members_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="members_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Members",
                "permissions": [
                    ("approve_member", "Can toggle approval status of member")
                ],
            },
        ),
        migrations.CreateModel(
            name="MemberBranch",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_of_membership", models.DateField()),
                (
                    "branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="member_branch",
                        to="branch.branch",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="member_branches",
                        to="accounts.member",
                    ),
                ),
            ],
            options={
                "verbose_name": "Member Branch",
                "verbose_name_plural": "Member Branches",
                "unique_together": {("member", "branch")},
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bio", models.TextField(blank=True, max_length=1024, null=True)),
                (
                    "contact",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="valid nepali phone number",
                        max_length=128,
                        null=True,
                        region=None,
                        unique=True,
                    ),
                ),
                ("birth_date", models.DateField(blank=True, null=True)),
                (
                    "current_city",
                    models.CharField(blank=True, max_length=512, null=True),
                ),
                ("home_town", models.CharField(blank=True, max_length=512, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True)),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="country_followers",
                        to="location.country",
                    ),
                ),
                (
                    "district",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="district_followers",
                        to="location.district",
                    ),
                ),
                (
                    "province",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="province_followers",
                        to="location.province",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Follower Profile",
                "verbose_name_plural": "Follower Profiles",
            },
        ),
        migrations.CreateModel(
            name="ResetPasswordCode",
            fields=[
                (
                    "code",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reset_password_codes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Reset Password Codes",
            },
        ),
        migrations.CreateModel(
            name="ProfileImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=accounts.sub_models.profile.upload_profile_image_to,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "JPG"]
                            )
                        ],
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile_images",
                        to="accounts.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Follower Profile Image",
                "verbose_name_plural": "Follower Profile Images",
            },
        ),
        migrations.CreateModel(
            name="MemberRole",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role_name",
                    models.CharField(
                        choices=[
                            ("Branch Chief", "Branch Chief"),
                            ("Branch Vice Chief", "Branch Vice Chief"),
                            ("Leader", "Leader"),
                            ("Double Star Leader", "Double Star Leader"),
                            ("Single Star Leader", "Single Star Leader"),
                            ("Maintainer", "Maintainer"),
                        ],
                        max_length=18,
                    ),
                ),
                ("from_date", models.DateField()),
                ("to_date", models.DateField()),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="member_roles",
                        to="accounts.member",
                    ),
                ),
                (
                    "member_branch",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="member_branch_roles",
                        to="accounts.memberbranch",
                    ),
                ),
            ],
            options={
                "verbose_name": "Member Role",
                "verbose_name_plural": "Member Roles",
                "unique_together": {("member", "role_name", "member_branch")},
            },
        ),
    ]
