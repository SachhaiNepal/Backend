from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField



class AdFile(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, unique = True)
    image = models.ImageField(upload_to="ad_file", null=True, blank=True)
    phone = PhoneNumberField(unique=True, max_length=20)
    name = models.CharField( max_length=50)



