from rest_framework import serializers

from accounts.models import Member
from accounts.serializers.member_branch import MemberBranchListSerializer
from accounts.serializers.member_role import MemberRoleListSerializer


class MemberSerializer(serializers.ModelSerializer):
    member_roles = MemberRoleListSerializer(many=True)
    member_branches = MemberBranchListSerializer(many=True)

    class Meta:
        model = Member
        fields = [
            "id", "user",
            "is_approved", "approved_by", "approved_at",
            "created_by", "created_at",
            "updated_by", "updated_at",
            "member_roles", "member_branches"
        ]
        depth = 1


class MemberPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return Member.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.updated_by = self.context["request"].user
        return super().update(instance, validated_data)
