from rest_framework import serializers

from accounts.models import Profile, ProfileImage


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProfileImage
        fields = "__all__"


class ProfileImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    profile_images = ProfileImageSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        exclude = ["user"]
        depth = 1


class ProfilePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
