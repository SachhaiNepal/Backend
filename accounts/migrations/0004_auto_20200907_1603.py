# Generated by Django 3.1 on 2020-09-07 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('location', '0001_initial'),
        ('accounts', '0003_auto_20200907_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='municipality_ward_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='MemberMunicipalityWardNo', to='location.municipalitywardnumber'),
        ),
        migrations.AddField(
            model_name='member',
            name='vdc_ward_no',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='MemberVdcWardNo', to='location.vdcwardnumber'),
        ),
        migrations.AlterField(
            model_name='member',
            name='vdc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    related_name='MemberVdc', to='location.vdc'),
        ),
    ]
