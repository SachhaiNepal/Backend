from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Profile
from accounts.serializers.profile import ProfileSerializer
from location.models import Country, District, Province


class RegisterFollowerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=20, required=True)
    username = serializers.CharField(
        max_length=20,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
        required=True,
    )
    contact = PhoneNumberField(
        validators=[UniqueValidator(queryset=Profile.objects.all())],
        required=False,
        allow_blank=True,
    )
    password = serializers.CharField(max_length=20, required=True)
    confirm_password = serializers.CharField(max_length=20, required=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    current_city = serializers.CharField(max_length=64, required=False, allow_null=True)
    home_town = serializers.CharField(max_length=64, required=False, allow_null=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), required=False
    )
    province = serializers.PrimaryKeyRelatedField(
        queryset=Province.objects.all(), required=False
    )
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(), required=False
    )

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def validate(self, validated_data):
        if validated_data["password"] != validated_data["confirm_password"]:
            raise serializers.ValidationError("Password & confirm password must match.")
        return validated_data

    def create(self, validated_data):
        return validated_data


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        # do not create admins from this api
        read_only_fields = ["is_active", "date_joined", "is_superuser", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    last_login = serializers.SerializerMethodField()
    date_joined = serializers.SerializerMethodField()

    @staticmethod
    def get_date_joined(obj):
        return obj.date_joined.strftime("%d %B, %Y") if obj.date_joined else None

    @staticmethod
    def get_last_login(obj):
        return obj.last_login.strftime("%d %B %Y, %I:%M %p") if obj.last_login else None

    class Meta:
        model = get_user_model()
        depth = 1
        fields = (
            "date_joined",
            "email",
            "first_name",
            "groups",
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "last_name",
            "user_permissions",
            "username",
            "profile",
        )
