from rest_framework import serializers

from accounts.models import Member
from accounts.serializers.member_branch import MemberBranchListSerializer


class MemberSerializer(serializers.ModelSerializer):
    member_branches = MemberBranchListSerializer(many=True)
    approved_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    @staticmethod
    def get_approved_at(obj):
        return obj.approved_at.strftime("%d %B, %Y") if obj.approved_at else None

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime("%d %B, %Y") if obj.created_at else None

    @staticmethod
    def get_updated_at(obj):
        return obj.updated_at.strftime("%d %B, %Y") if obj.updated_at else None

    class Meta:
        model = Member
        fields = [
            "id",
            "user",
            "is_approved",
            "approved_by",
            "approved_at",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "member_branches",
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
