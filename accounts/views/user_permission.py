from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.permissions import AssignPermissionSerializer, UserPermissionSerializer
from accounts.serializers.user import UserSerializer, UserWithProfileSerializer


def get_permission_string(permission):
    n_k = permission.natural_key()
    return '{}.{}'.format(n_k[1], n_k[0])


class UserPermission:
    def __init__(self, item_id, name, codename, content_type, assigned):
        self.id = item_id
        self.name = name
        self.codename = codename
        self.content_type = content_type
        self.is_assigned = assigned


class ListUserPermission(APIView):

    def post(self, request):
        serializer = AssignPermissionSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.get(pk=serializer.data.get("user"))
            permission = Permission.objects.get(pk=serializer.data.get("permission"))
            if not user.has_perm(get_permission_string(permission)):
                user.user_permissions.add(permission)
                user.save()
                user_serializer = UserWithProfileSerializer(user, read_only=True)
                return Response({
                    "detail": "User permission added",
                    "user"  : user_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "permission": ["Permission already assigned"]
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = AssignPermissionSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model().objects.get(pk=serializer.data.get("user"))
            permission = Permission.objects.get(pk=serializer.data.get("permission"))
            if user.has_perm(get_permission_string(permission)):
                user.user_permissions.remove(permission)
                user.save()
                user_serializer = UserSerializer(user)
                return Response({
                    "detail": "User permission removed",
                    "user"  : user_serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "permission": ["Permission is not assigned"]
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPermissionDetail(APIView):

    @staticmethod
    def is_permission_assigned_to_user(user, permission):
        return user.has_perm(get_permission_string(permission))

    @staticmethod
    def get_content_type_grouped_permissions(serializer):
        """:param serializer PermissionSerializer"""
        content_type_array = []
        response_dict = { }
        for permission in serializer.data:
            content_type_id = permission.get('content_type')
            content_type = ContentType.objects.get(pk=content_type_id)
            app = content_type.app_label
            if not app in content_type_array:
                response_dict[app] = []
                content_type_array.append(app)
            response_dict[app].append(permission)
        return response_dict

    def get(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        permissions = Permission.objects.all()
        user_permissions = []
        for permission in permissions:
            user_permission = UserPermission(
                item_id=permission.id,
                name=permission.name,
                codename=permission.codename,
                content_type=permission.content_type.id,
                assigned=self.is_permission_assigned_to_user(user, permission)
            )
            user_permissions.append(user_permission)

        serializer = UserPermissionSerializer(user_permissions, many=True)
        grouped_permissions = self.get_content_type_grouped_permissions(serializer)

        return Response({
            "models": len(grouped_permissions),
            "data"  : grouped_permissions
        }, status=status.HTTP_200_OK)
