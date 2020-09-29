# Generated by Django 3.1 on 2020-09-06 10:19

import django.db.models.deletion
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('address', models.CharField(max_length=512, unique=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=15, region=None, unique=True)),
                ('is_main', models.BooleanField(default=False, verbose_name='Is Main Branch')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='BranchCountry',
                                   to='location.country')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING,
                                                 related_name='Creator', to=settings.AUTH_USER_MODEL)),
                ('district',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='BranchDistrict',
                                   to='location.district')),
                ('province',
                 models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='BranchProvince',
                                   to='location.province')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True,
                                                 on_delete=django.db.models.deletion.DO_NOTHING,
                                                 related_name='Modifier', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
