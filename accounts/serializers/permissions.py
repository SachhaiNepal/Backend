from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        depth = 1


class AssignPermissionSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all()
    )
    permission = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all()
    )


class UserPermissionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    codename = serializers.CharField()
    content_type = serializers.IntegerField()
    is_assigned = serializers.BooleanField()

