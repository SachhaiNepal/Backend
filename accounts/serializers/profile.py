from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    def validate(self, attrs):
        vdc = attrs.get("vdc")
        municipality = attrs.get("municipality")
        vdc_ward = attrs.get("vdc_ward")
        municipality_ward = attrs.get("municipality_ward")
        if (vdc and municipality) or (vdc_ward and municipality_ward):
            raise ValidationError(
                "Both municipality and vdc fields cannot be selected."
            )
        elif municipality and vdc_ward:
            raise ValidationError("Cannot assign vdc ward for a municipality.")
        elif vdc and municipality_ward:
            raise ValidationError("Cannot assign municipality ward for a vdc.")
        return attrs
