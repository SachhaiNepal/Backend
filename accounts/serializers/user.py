import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Profile, ProfileImage, CoverImage
from accounts.serializers.member import UserMemberSerializer
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    member = UserMemberSerializer()
    active_profile_image = serializers.SerializerMethodField()
    active_cover_image = serializers.SerializerMethodField()

    @staticmethod
    def generate_url_for_media_resource(media_url):
        front = "http" if os.getenv("IS_SECURE") else "https"
        return "{}://{}{}".format(
            front, os.getenv("BASE_URL"), media_url
        )

    def get_active_profile_image(self, obj):
        profile = obj.profile
        active_profile_image = ProfileImage.objects.filter(active=True, profile=profile)
        if active_profile_image.count() > 0:
            return self.generate_url_for_media_resource(active_profile_image.first().image.url)
        return None

    def get_active_cover_image(self, obj):
        profile = obj.profile
        active_cover_image = CoverImage.objects.filter(active=True, profile=profile)
        if active_cover_image.count() > 0:
            return self.generate_url_for_media_resource(active_cover_image.first().image.url)
        return None

    class Meta:
        model = get_user_model()
        depth = 1
        fields = "__all__"
