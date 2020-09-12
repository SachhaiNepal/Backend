from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from branch.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Branch.objects.all(),
                fields=[
                    "country",
                    "province",
                    "district",
                    "municipality",
                    "municipality_ward_no",
                    "vdc",
                    "vdc_ward_no",
                ]
            )
        ]

    # object level validation
    def validate(self, data):
        """
        Check if both vdc and municipality are selected
        """
        if data["municipality"] and data["vdc"]:
            raise serializers.ValidationError("Both municipality and vdc cannot be assigned.")
        if data["municipality_ward_no"] and data["vdc_ward_no"]:
            raise serializers.ValidationError("Both municipality and vdc numbers cannot be assigned.")
        return data

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        branch = Branch.objects.create(**validated_data)
        return branch

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        instance.save()
        return instance
