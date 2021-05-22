from rest_framework import serializers

from accounts.models import MemberBranch
from accounts.serializers.member_role import MemberRoleListSerializer


class MemberBranchListSerializer(serializers.ModelSerializer):
    member_branch_roles = MemberRoleListSerializer(many=True, read_only=True)

    class Meta:
        model = MemberBranch
        fields = (
            "id",
            "member",
            "branch",
            "date_of_membership",
            "member_branch_roles"
        )
        depth = 1


class MemberBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberBranch
        fields = "__all__"
