from rest_framework import serializers

from accounts.models import MemberRole, MemberBranch
from branch.models import Branch


# class MemberRoleListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MemberRole
#         fields = "__all__"
#         depth = 1


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
            if member_branch.branch == branch_id:
                found = True
        if not found:
            raise serializers.ValidationError(
                "Member not registered in selected branch."
            )
        return data
