from rest_framework import serializers

from accounts.models import ProfileImage, Profile


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProfileImage
        fields = ["image"]


class ProfileImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    profile_images = ProfileImageSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "bio", "contact", "birth_date",
            "current_city", "home_town",
            "country", "province", "district",
            "last_updated",
            "profile_images",
        )
        depth = 1


class ProfilePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
