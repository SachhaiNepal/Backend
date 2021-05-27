from rest_framework import serializers

from accounts.models import Member
from accounts.serializers.member_branch import MemberBranchListSerializer


class UserMemberSerializer(serializers.ModelSerializer):
    member_branches = MemberBranchListSerializer(many=True)

    class Meta:
        model = Member
        exclude = ["user"]
        depth = 1


class MemberSerializer(serializers.ModelSerializer):
    member_branches = MemberBranchListSerializer(many=True)

    class Meta:
        model = Member
        fields = "__all__"
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
