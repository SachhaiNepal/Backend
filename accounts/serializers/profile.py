from rest_framework import serializers

from accounts.models import Profile, ProfileImage
from accounts.sub_models.profile import CoverImage


class CoverImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverImage
        fields = "__all__"


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    profile_images = ProfileImageSerializer(many=True, read_only=True)
    cover_images = CoverImagePostSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        exclude = ["user"]
        depth = 1


class ProfilePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
