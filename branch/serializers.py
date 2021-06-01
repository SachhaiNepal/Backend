from rest_framework import serializers

from branch.models import Branch


class BranchSerializer(serializers.ModelSerializer):
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
        municipality = data.get("municipality")
        vdc = data.get("vdc")
        municipality_ward = data.get("municipality_ward")
        vdc_ward = data.get("vdc_ward")

        if not municipality and not vdc:
            raise serializers.ValidationError(
                "One of the municipality or vdc must be assigned."
            )
        if not municipality_ward and not vdc_ward:
            raise serializers.ValidationError(
                "One of the municipality or vdc ward must be assigned."
            )
        if municipality and vdc:
            raise serializers.ValidationError(
                "Both municipality and vdc cannot be assigned."
            )
        if municipality_ward and vdc_ward:
            raise serializers.ValidationError(
                "Both municipality or vdc ward cannot be assigned."
            )
        if municipality and vdc_ward:
            raise serializers.ValidationError(
                "Municipality and vdc ward is not an expected location combination."
            )
        if vdc and municipality_ward:
            raise serializers.ValidationError(
                "Vdc and municipality ward is not an expected location combination."
            )
        return data

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Branch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)
