# Generated by Django 3.1.3 on 2020-11-24 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_remove_district_country'),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='municipality_ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='EventMunicipalityWardNumber', to='location.municipalityward'),
        ),
        migrations.AlterField(
            model_name='event',
            name='vdc_ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='EventVdcWardNumber', to='location.vdcward'),
        ),
    ]
