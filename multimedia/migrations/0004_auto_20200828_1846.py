# Generated by Django 3.1 on 2020-08-28 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multimedia', '0003_auto_20200823_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='approved_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='MultimediaApprover', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='media',
            name='uploaded_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='MediaUploader', to=settings.AUTH_USER_MODEL),
        ),
    ]
