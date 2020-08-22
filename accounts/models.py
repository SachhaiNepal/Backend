from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from branch.models import Branch
from utils.choices import COUNTRY_CHOICES, DISTRICT_CHOICES


class MemberManager(BaseUserManager):
    use_in_migrations = True

    def __create_user(self, email, password, is_staff, **kwargs):
        if not email:
            raise ValueError("email address field is required!")
        if not password:
            raise ValueError("password field is required!")

        email = self.normalize_email(email)
        member = self.model(
            email=email,
            is_staff=is_staff,
            **kwargs
        )
        member.set_password(password)
        member.save(using=self._db)
        return member

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.__create_user(email, password, True, **extra_fields)
        return user


class Member(AbstractBaseUser):
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
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

    is_staff = models.BooleanField(default=False, verbose_name="Is Admin")
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    approved_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="Approver"
    )
    approved_at = models.DateTimeField(default=None, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MemberManager()

    USERNAME_FIELD = "email"

    # REQUIRED_FIELDS = [
    # ]

    class Meta:
        verbose_name_plural = "Members"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, package_name):
        return True
