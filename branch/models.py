from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

COUNTRY_CHOICES = (
    ("AFG", "Afghanistan"),
    ("IND", "India"),
    ("PAK", "Pakistan"),
    ("BAN", "Bangladesh"),
    ("SRI", "Sri Lanka"),
    ("NEP", "Nepal"),
    ("BHU", "Bhutan"),
    ("MAL", "Maldives")
)

DISTRICT_CHOICES = (
    ("BHOJPUR", "Bhojpur"),
    ("DHANKUTA", "Dhankuta"),
    ("ILAM", "Ilam"),
    ("JHAPA", "Jhapa"),
    ("KHOTANG", "Khotang"),
    ("MORANG", "Morang"),
    ("OKHALDHUNGA", "Okhaldhunga"),
    ("PANCHTHAR", "Panchthar"),
    ("SANKHUWASABHA", "Sankhuwasabha"),
    ("SOLUKHUMBU", "Solukhumbu"),
    ("SUNSARI", "Sunsari"),
    ("TAPLEJUNG", "Taplejung"),
    ("TERATHUM", "Terhathum"),
    ("UDAYAPUR", "Udayapur"),

    ("BARA", "Bara"),
    ("PARSA", "Parsa"),
    ("DHANUSHA", "Dhanusha"),
    ("MAHOTTARI", "Mahottari"),
    ("RAUTAHAT", "Rautahat"),
    ("SAPTARI", "Saptari"),
    ("SARLAHI", "Sarlahi"),
    ("SIRAHA", "Siraha"),

    ("BHAKTAPUR", "Bhaktapur"),
    ("CHITWAN", "Chitwan"),
    ("DHADING", "Dhading"),
    ("DOLAKHA", "Dolakha"),
    ("KATHMANDU", "Kathmandu"),
    ("KAVREPALANCHOK", "Kavrepalanchok"),
    ("LALITPUR", "Lalitpur"),
    ("MAKWANPUR", "Makwanpur"),
    ("NUWAKOT", "Nuwakot"),
    ("RAMECHHAP", "Ramechhap"),
    ("RASUWA", "Rasuwa"),
    ("SINDHULI", "Sindhuli"),
    ("SINDHUPALCHOK", "Sindhupalchok"),

    ("BAGLUNG", "Baglung"),
    ("GORKHA", "Gorkha"),
    ("KASKI", "Kaski"),
    ("LAMJUNG", "Lamjung"),
    ("MANANG", "Manang"),
    ("MUSTANG", "Mustang"),
    ("MYAGDI", "Myagdi"),
    ("NAWALPUR", "Nawalpur"),
    ("PARBAT", "Parbat"),
    ("SYANGJA", "Syangja"),
    ("TANAHUN", "Tanahun"),

    ("ARGHAKHACHI", "Arghakhanchi"),
    ("BANKE", "Banke"),
    ("BARDIYA", "Bardiya"),
    ("DANG", "Dang"),
    ("RUKUM", "Rukum"),
    ("GULMI", "Gulmi"),
    ("KAPILAVASTU", "Kapilavastu"),
    ("PARASI", "Parasi"),
    ("PALPA", "Palpa"),
    ("PYUTHAN", "Pyuthan"),
    ("ROLPA", "Rolpa"),
    ("RUPANDEHI", "Rupandehi"),

    ("DAILEKH", "Dailekh"),
    ("DOLPA", "Dolpa"),
    ("HUMLA", "Humla"),
    ("JAJARKOT", "Jajarkot"),
    ("JUMLA", "Jumla"),
    ("KALIKOT", "Kalikot"),
    ("MUGU", "Mugu"),
    ("SALYAN", "Salyan"),
    ("SURKHET", "Surkhet"),
    ("RUKUM", "Rukum"),

    ("ACHHAM", "Achham"),
    ("BAITADI", "Baitadi"),
    ("BAJHANG", "Bajhang"),
    ("BAJURA", "Bajura"),
    ("DADELDHURA", "Dadeldhura"),
    ("DARCHULA", "Darchula"),
    ("DOTI", "Doti"),
    ("KAILALI", "Kailali"),
    ("KANCHANPUR", "Kanchanpur")
)


class MemberManager(BaseUserManager):
    use_in_migrations = True

    def __create_user(self, email, password, state, is_admin, **kwargs):
        if not email:
            raise ValueError("email address field is required!")
        if not password:
            raise ValueError("password field is required!")

        email = self.normalize_email(email)
        member = self.model(
            email=email,
            is_admin=is_admin,
            state=state,
            **kwargs
        )
        member.set_password(password)
        member.save(using=self._db)
        return member

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.__create_user(email, password, True, True, **extra_fields)
        user.save()
        return user


class Member(AbstractBaseUser):
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=512, blank=True, null=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, null=True, blank=True)
    district = models.CharField(max_length=14, choices=DISTRICT_CHOICES, null=True)
    phone = models.BigIntegerField(unique=True, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    state = models.BooleanField(default=False)

    created_by = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="Creator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="Modifier")
    updated_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="Approver")
    approved_at = models.DateTimeField(auto_now_add=True)

    objects = MemberManager()

    USERNAME_FIELD = "email"

    # REQUIRED_FIELDS = [
    # ]

    class Meta:
        verbose_name_plural = "Members"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, package_name):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True
