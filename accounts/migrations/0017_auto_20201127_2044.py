# Generated by Django 3.1.3 on 2020-11-27 14:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0015_auto_20201127_2044'),
        ('accounts', '0016_profileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='branch',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Branch', to='branch.branch'),
            preserve_default=False,
        ),
    ]
