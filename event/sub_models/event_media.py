from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from backend.settings import ALLOWED_IMAGES_EXTENSIONS, MAX_UPLOAD_IMAGE_SIZE
from event.sub_models.event import Event


class EventPhoto(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to="event/photos",
        validators=[FileExtensionValidator(ALLOWED_IMAGES_EXTENSIONS)],
    )

    def __str__(self):
        return "{} - {}".format(self.event.title, self.image.name)

    def clean(self):
        if self.image.size / 1000 > MAX_UPLOAD_IMAGE_SIZE:
            raise ValidationError("Image size exceeds max image upload size.")

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)


class EventVideoUrls(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="video_urls"
    )
    video_url = models.URLField(unique=True)

    def __str__(self):
        return self.video_url
