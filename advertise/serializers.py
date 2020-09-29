from rest_framework import serializers

from advertise.models import Advertisement
from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from utils.file import check_size


class AdFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = "__all__"

    def validate_image(self, obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["modified_by"] = self.context["request"].user
        return Advertisement.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.modified_by = self.context["request"].user
        return super().update(instance, validated_data)
