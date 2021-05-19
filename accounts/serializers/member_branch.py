from rest_framework import serializers

from accounts.models import MemberBranch
from branch.models import Branch


class MemberBranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberBranch
        fields = "__all__"
        depth = 1


class MemberBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberBranch
        fields = "__all__"

    @staticmethod
    def validate_branch(value):
        try:
            Branch.objects.get(pk=value)
            return value
        except Branch.DoesNotExist:
            raise serializers.ValidationError("Branch does not exist.")
