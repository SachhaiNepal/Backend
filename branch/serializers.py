from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from branch.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        depth = 1


class BranchPostSerializer(serializers.ModelSerializer):
    contacts = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = Branch
        fields = "__all__"

    # object level validation
    def validate(self, data):
        """
        Check if both vdc and municipality are selected
        """
        try:
            check = data['municipality']
            try:
                check = data['vdc']
                raise serializers.ValidationError("Both municipality and vdc cannot be assigned.")
            except KeyError:
                return data
        except KeyError:
            try:
                check = data['vdc']
                return data
            except KeyError:
                raise serializers.ValidationError("One of the municipality or vdc must be assigned.")

    def create(self, validated_data):
        # TODO: add context request user
        validated_data["created_by"] = get_user_model().objects.get(id=1)
        if validated_data["is_approved"]:
            # validated_data["approved_by"] = self.context["request"].user
            validated_data["approved_at"] = timezone.now()
        return Branch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.updated_by = self.context["request"].user
        if not instance.is_approved and validated_data["is_approved"]:
            # validated_data["approved_by"] = self.context["request"].user
            validated_data["approved_at"] = timezone.now()
        if not validated_data["is_approved"] and instance.is_approved:
            validated_data["approved_by"] = None
            validated_data["approved_at"] = None
        return super().update(instance, validated_data)
