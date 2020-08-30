from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"
        depth = 1


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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)


class LogoutSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)


class UpdatePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_new_password(password):
        validate_password(password)
        return password

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("New password must match with confirm password.")
        if data["confirm_password"] == data["password"]:
            raise serializers.ValidationError("New and old password must not be same.")
        return data


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    @staticmethod
    def validate_new_password(new_password):
        validate_password(new_password)
        return new_password

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("New password must match with confirm password.")
        return data
