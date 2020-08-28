from rest_framework import serializers

from branch.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        branch = Branch.objects.create(**validated_data)
        return branch

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        instance.save()
        return instance
