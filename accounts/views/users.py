from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import (
    UserCreateSerializer, UserUpdateSerializer, UserWithProfileSerializer
)


class ListFollower(APIView):
    """
    View to list all users in the system.
    * Only staff users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        """
        Return a list of all users.
        """
        context = {"request": request}
        users = User.objects.all()
        return Response(
            UserWithProfileSerializer(users, many=True, context=context).data,
            status=status.HTTP_200_OK
        )

    @staticmethod
    def post(request):
        """
        Creates a brand new user-member(x)
        """
        context = { "request": request }
        serializer = UserCreateSerializer(
            data=request.data, context=context
        )

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(
                UserWithProfileSerializer(user, context=context).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    User Detailed Operations
    * Only staff users are able to access this view.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(get_user_model(), pk=pk)

    def get(self, request, pk):
        """
        Returns single user by pk
        """
        context = { "request": request }
        user = self.get_object(pk)
        return Response(
            UserWithProfileSerializer(user, context=context).data,
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        """
        Updates user by pk
        """
        context = { "request": request }
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(
            user, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User updated successfully.",
                    "data": UserWithProfileSerializer(self.get_object(pk), context=context).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies user by pk
        """
        context = { "request": request }
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User patched successfully.",
                    "data": UserWithProfileSerializer(self.get_object(pk), context=context).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(
            {"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
