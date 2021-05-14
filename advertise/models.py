from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE


class Advertisement(models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(
        upload_to="advertise",
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )
    phone = PhoneNumberField(unique=True)
    owner = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="ads_created",
        editable=False,
    )
    modified_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="ads_modified",
        editable=False,
    )

    def __str__(self):
        return self.owner

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pk:
            this_record = Advertisement.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        super(Advertisement, self).save(
            force_insert, force_update, using, update_fields
        )

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)
