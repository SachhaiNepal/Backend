# Generated by Django 3.1 on 2020-08-23 13:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
                ('country', models.CharField(blank=True, choices=[('AFG', 'Afghanistan'), ('IND', 'India'), ('PAK', 'Pakistan'), ('BAN', 'Bangladesh'), ('SRI', 'Sri Lanka'), ('NEP', 'Nepal'), ('BHU', 'Bhutan'), ('MAL', 'Maldives')], max_length=3, null=True)),
                ('district', models.CharField(choices=[('BHOJPUR', 'Bhojpur'), ('DHANKUTA', 'Dhankuta'), ('ILAM', 'Ilam'), ('JHAPA', 'Jhapa'), ('KHOTANG', 'Khotang'), ('MORANG', 'Morang'), ('OKHALDHUNGA', 'Okhaldhunga'), ('PANCHTHAR', 'Panchthar'), ('SANKHUWASABHA', 'Sankhuwasabha'), ('SOLUKHUMBU', 'Solukhumbu'), ('SUNSARI', 'Sunsari'), ('TAPLEJUNG', 'Taplejung'), ('TERATHUM', 'Terhathum'), ('UDAYAPUR', 'Udayapur'), ('BARA', 'Bara'), ('PARSA', 'Parsa'), ('DHANUSHA', 'Dhanusha'), ('MAHOTTARI', 'Mahottari'), ('RAUTAHAT', 'Rautahat'), ('SAPTARI', 'Saptari'), ('SARLAHI', 'Sarlahi'), ('SIRAHA', 'Siraha'), ('BHAKTAPUR', 'Bhaktapur'), ('CHITWAN', 'Chitwan'), ('DHADING', 'Dhading'), ('DOLAKHA', 'Dolakha'), ('KATHMANDU', 'Kathmandu'), ('KAVREPALANCHOK', 'Kavrepalanchok'), ('LALITPUR', 'Lalitpur'), ('MAKWANPUR', 'Makwanpur'), ('NUWAKOT', 'Nuwakot'), ('RAMECHHAP', 'Ramechhap'), ('RASUWA', 'Rasuwa'), ('SINDHULI', 'Sindhuli'), ('SINDHUPALCHOK', 'Sindhupalchok'), ('BAGLUNG', 'Baglung'), ('GORKHA', 'Gorkha'), ('KASKI', 'Kaski'), ('LAMJUNG', 'Lamjung'), ('MANANG', 'Manang'), ('MUSTANG', 'Mustang'), ('MYAGDI', 'Myagdi'), ('NAWALPUR', 'Nawalpur'), ('PARBAT', 'Parbat'), ('SYANGJA', 'Syangja'), ('TANAHUN', 'Tanahun'), ('ARGHAKHACHI', 'Arghakhanchi'), ('BANKE', 'Banke'), ('BARDIYA', 'Bardiya'), ('DANG', 'Dang'), ('RUKUM', 'Rukum'), ('GULMI', 'Gulmi'), ('KAPILAVASTU', 'Kapilavastu'), ('PARASI', 'Parasi'), ('PALPA', 'Palpa'), ('PYUTHAN', 'Pyuthan'), ('ROLPA', 'Rolpa'), ('RUPANDEHI', 'Rupandehi'), ('DAILEKH', 'Dailekh'), ('DOLPA', 'Dolpa'), ('HUMLA', 'Humla'), ('JAJARKOT', 'Jajarkot'), ('JUMLA', 'Jumla'), ('KALIKOT', 'Kalikot'), ('MUGU', 'Mugu'), ('SALYAN', 'Salyan'), ('SURKHET', 'Surkhet'), ('RUKUM', 'Rukum'), ('ACHHAM', 'Achham'), ('BAITADI', 'Baitadi'), ('BAJHANG', 'Bajhang'), ('BAJURA', 'Bajura'), ('DADELDHURA', 'Dadeldhura'), ('DARCHULA', 'Darchula'), ('DOTI', 'Doti'), ('KAILALI', 'Kailali'), ('KANCHANPUR', 'Kanchanpur')], max_length=14, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Approver', to='accounts.member')),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Branch', to='branch.branch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Members',
            },
        ),
    ]
