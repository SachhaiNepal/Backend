from rest_framework import serializers

from accounts.models import MemberRole, MemberBranch
from branch.models import Branch


class MemberRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRole
        fields = "__all__"

    def validate_branch(self, value):
        try:
            Branch.objects.get(pk=value)
            return value
        except Branch.DoesNotExist:
            raise serializers.ValidationError("Branch does not exist.")

    def validate(self, data):
        member = data["member"]
        branch_id = data["branch"]
        member_branches = MemberBranch.objects.filter(member=member)
        found = False
        for member_branch in member_branches:
            if member_branch.id == branch_id:
                found = True
        if not found:
            raise serializers.ValidationError(
                "Member not registered in selected branch."
            )
        return data
