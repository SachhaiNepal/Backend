# Generated by Django 3.1 on 2020-09-06 10:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RelatedCountryForDistrict', to='location.country')),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RelatedMunicipalityForDistrict', to='location.district')),
            ],
            options={
                'verbose_name_plural': 'Municipalities',
            },
        ),
        migrations.CreateModel(
            name='VDC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RelatedVDCForDistrict', to='location.district')),
            ],
            options={
                'verbose_name_plural': 'VDCs',
            },
        ),
        migrations.CreateModel(
            name='VDCWardNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('number', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(40), django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vdc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RelatedWardNumberForVDC', to='location.vdc')),
            ],
            options={
                'verbose_name_plural': 'VDC Wards',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('number', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RelatedCountryForProvince', to='location.country')),
            ],
        ),
        migrations.CreateModel(
            name='MunicipalityWardNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('number', models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(40), django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RelatedWardNumberForMunicipality', to='location.municipality')),
            ],
            options={
                'verbose_name_plural': 'Municipality Wards',
            },
        ),
        migrations.AddField(
            model_name='district',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RelatedProvince', to='location.province'),
        ),
    ]
