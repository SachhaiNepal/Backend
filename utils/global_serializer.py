import os

from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.sub_models.profile import ProfileImage, CoverImage


class UserWithActiveProfileMediaSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    active_profile_image = serializers.SerializerMethodField()
    active_cover_image = serializers.SerializerMethodField()

    @staticmethod
    def generate_url_for_media_resource(media_url):
        front = "http" if os.getenv("IS_SECURE") else "https"
        return "{}://{}{}".format(
            front, os.getenv("BASE_URL"), media_url
        )

    @staticmethod
    def get_full_name(obj):
        if not obj.first_name and not obj.last_name:
            return None
        elif not obj.first_name and obj.last_name:
            return obj.last_name
        elif obj.first_name and not obj.last_name:
            return obj.first_name
        else:
            return "{} {}".format(obj.first_name, obj.last_name)

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
        fields = ["id", "full_name", "username", "active_profile_image", "active_cover_image"]
