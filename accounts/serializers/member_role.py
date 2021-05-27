from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import MemberBranch, MemberRole
from accounts.sub_models.member import Member


class MemberRoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberRole
        exclude = ["member", "member_branch"]
        depth = 2


class MemberRoleSerializer(serializers.ModelSerializer):
    def validate(self, validated_data):
        from_date = validated_data.get("from_date")
        to_date = validated_data.get("to_date")
        if from_date > to_date or from_date == to_date:
            raise ValidationError("To date must be smaller than from date.")
        return validated_data

    class Meta:
        model = MemberRole
        fields = "__all__"
