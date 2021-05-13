from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Member, MemberBranch, MemberRole, Profile, ProfileImage
from branch.models import Branch
from location.models import Country, Province, District


class MemberSerializer(serializers.ModelSerializer):
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


class RegisterFollowerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=20, required=True)
    last_name = serializers.CharField(max_length=20, required=True)
    username = serializers.CharField(
        max_length=20,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
        required=True
    )
    email = serializers.EmailField(validators=[UniqueValidator(queryset=get_user_model().objects.all())], required=True)
    contact = PhoneNumberField(validators=[UniqueValidator(queryset=Profile.objects.all())], required=False, allow_blank=True)
    password = serializers.CharField(max_length=20, required=True)
    confirm_password = serializers.CharField(max_length=20, required=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    current_city = serializers.CharField(max_length=64, required=False, allow_null=True)
    home_town = serializers.CharField(max_length=64, required=False, allow_null=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), required=False)
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), required=False)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=False)

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def validate(self, validated_data):
        if validated_data["password"] != validated_data["confirm_password"]:
            raise serializers.ValidationError("Password & confirm password must match.")
        return validated_data

    def create(self, validated_data):
        return validated_data


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
        # do not create admins from this api
        read_only_fields = ["is_active", "date_joined", "is_superuser", "is_staff"]
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_password(password):
        validate_password(password)
        return password

    def create(self, validated_data):
        user = get_user_model().objects.create(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")


class ProfileImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ProfileImage
        fields = ["image"]


class ProfileImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    profile_images = ProfileImageSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            "bio",
            "contact",
            "birth_date",
            "current_city",
            "home_town",
            "country",
            "province",
            "district",
            "last_updated",
            "profile_images"
        )
        depth = 1


class ProfilePOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        depth = 1
        fields = (
            "date_joined",
            "email",
            "first_name",
            "groups",
            "id",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "last_name",
            "user_permissions",
            "username",
            "profile",
        )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64)


class LogoutSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64)


class UpdatePasswordSerializer(serializers.Serializer):
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


class MemberBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberBranch
        fields = "__all__"

    def validate_branch(self, value):
        try:
            Branch.objects.get(pk=value)
            return value
        except Branch.DoesNotExist:
            raise serializers.ValidationError("Branch does not exist.")


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
        member = data['member']
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
