# Generated by Django 3.1.1 on 2020-09-13 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20200912_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='country',
        ),
    ]
