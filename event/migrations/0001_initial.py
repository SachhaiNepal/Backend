# Generated by Django 3.1.8 on 2021-06-10 21:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import event.sub_models.event
import event.sub_models.event_media
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branch', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
                ('description', models.TextField(max_length=512, unique=True)),
                ('venue', models.CharField(max_length=64)),
                ('start_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('time_of_day', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening')], max_length=10)),
                ('type', models.CharField(choices=[('Satsang', 'Satsang'), ('General Meeting', 'General Meeting'), ('Board Meeting', 'Board Meeting')], max_length=15)),
                ('is_approved', models.BooleanField(default=False, editable=False)),
                ('is_main', models.BooleanField(default=False, editable=False)),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('approved_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='events_approved', to=settings.AUTH_USER_MODEL)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_events', to='branch.branch')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='country_events', to='location.country')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='events_created', to=settings.AUTH_USER_MODEL)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='district_events', to='location.district')),
                ('municipality', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='municipality_events', to='location.municipality')),
                ('municipality_ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='municipality_ward_events', to='location.municipalityward')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='province_events', to='location.province')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='events_updated', to=settings.AUTH_USER_MODEL)),
                ('vdc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vdc_events', to='location.vdc')),
                ('vdc_ward', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vdc_ward_events', to='location.vdcward')),
            ],
            options={
                'ordering': ('-created_at',),
                'permissions': [('approve_event', 'Can toggle approval status of event')],
            },
        ),
        migrations.CreateModel(
            name='EventVideoUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_url', models.URLField(unique=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_urls', to='event.event')),
            ],
            options={
                'verbose_name': 'Event Video URL',
                'verbose_name_plural': 'Event URLs',
            },
        ),
        migrations.CreateModel(
            name='EventVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(upload_to=event.sub_models.event_media.upload_event_video_to, validators=[django.core.validators.FileExtensionValidator(['webm', 'mp4', 'mpeg', 'flv'])])),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='event.event')),
            ],
            options={
                'verbose_name': 'Event Video',
                'verbose_name_plural': 'Event Videos',
            },
        ),
        migrations.CreateModel(
            name='EventPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=event.sub_models.event_media.upload_event_image_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='event.event')),
            ],
            options={
                'verbose_name': 'Event Image',
                'verbose_name_plural': 'Event Image',
            },
        ),
        migrations.CreateModel(
            name='EventInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('going', models.BooleanField(default=False, editable=False)),
                ('interested', models.BooleanField(default=False, editable=False)),
                ('attended', models.BooleanField(default=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='interested_event', to='event.event')),
                ('follower', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='interested_followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Interested Event',
                'verbose_name_plural': 'Interested Events',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EventComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_comments', to='event.event')),
                ('writer', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='follower_event_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Going Event',
                'verbose_name_plural': 'Going Events',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EventBannerImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=event.sub_models.event.upload_event_banner_to, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'JPG'])])),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banner_images', to='event.event')),
            ],
        ),
    ]
