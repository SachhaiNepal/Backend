from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ["user"]


class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ["user", "is_approved"]


class UserCreateSerializer(serializers.ModelSerializer):
    member = MemberCreateSerializer(many=False, read_only=False, required=False)

    class Meta:
        model = get_user_model()
        fields = "__all__"
        read_only_fields = ["is_active", "date_joined"]
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password

    def create(self, validated_data):
        member_data = validated_data.pop("member")
        user = get_user_model().objects.create(**validated_data)
        member = Member.objects.create(user=user, **member_data)
        if member.is_approved:
            member.approved_by = self.context["request"].user
            member.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "is_staff")
