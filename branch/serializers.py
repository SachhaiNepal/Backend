from rest_framework import serializers

from backend.settings import MAX_UPLOAD_IMAGE_SIZE
from branch.models import Branch, BranchImage
from utils.file import check_size
from utils.validate_location import validate_location


class BranchImageSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_image(obj):
        check_size(obj, MAX_UPLOAD_IMAGE_SIZE)
        return obj

    class Meta:
        model = BranchImage
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    images = BranchImageSerializer(many=True, read_only=True)

    class Meta:
        model = Branch
        fields = "__all__"
        depth = 1


class BranchPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        exclude = ["is_approved", "is_main"]

    # object level validation
    def validate(self, data):
        """
        Check if both vdc and municipality are selected
        """
        return validate_location(data)

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Branch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)
