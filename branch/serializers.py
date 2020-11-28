from rest_framework import serializers

from branch.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        depth = 1


class BranchPOSTSerializer(serializers.ModelSerializer):
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
        validated_data["created_by"] = self.context["request"].user
        return Branch.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)
