# Generated by Django 3.1.1 on 2020-09-29 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0009_auto_20200913_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='slogan',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
    ]
