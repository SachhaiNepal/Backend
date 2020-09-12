# Generated by Django 3.1.1 on 2020-09-12 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20200912_2141'),
        ('branch', '0006_auto_20200912_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='municipality_ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='BranchMunicipalityWardNo', to='location.municipalityward', unique=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='vdc_ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='BranchVdcWardNo', to='location.vdcward', unique=True),
        ),
    ]
