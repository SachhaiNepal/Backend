# Generated by Django 3.1 on 2020-09-07 10:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('branch', '0003_auto_20200907_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='branch'),
        ),
    ]
