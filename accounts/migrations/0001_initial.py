# Generated by Django 3.1 on 2020-09-06 10:19

import uuid

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
            name='ResetPasswordCode',
            fields=[
                ('code', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reset Password Codes',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temporary_address', models.CharField(blank=True, max_length=512, null=True)),
                ('permanent_address', models.CharField(blank=True, max_length=512, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField(blank=True, default=None, editable=False, null=True)),
                ('approved_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Approver', to=settings.AUTH_USER_MODEL)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='MemberCountry', to='location.country')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='MemberDistrict', to='location.district')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='MemberProvince', to='location.province')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Members',
            },
        ),
    ]
