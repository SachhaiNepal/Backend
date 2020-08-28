from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member
from accounts.serializers import UserCreateSerializer, UserUpdateSerializer, MemberUpdateSerializer, MemberSerializer


class ListUser(APIView):
    """
    View to list all users in the system.
    * Only staff users are able to access this view.
    """
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        """
        Return a list of all users.
        """
        users = User.objects.all()
        return Response(UserCreateSerializer(users, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        """
        Creates a brand new user-member(x)
        """
        serializer = UserCreateSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(UserCreateSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    User Detailed Operations
    * Only staff users are able to access this view.
    """
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        """
        Returns single user by pk
        """
        user = self.get_object(pk)
        return Response(UserCreateSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates user by pk
        """
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(
            user, data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies user by pk
        """
        user = self.get_object(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User patched successfully.",
                "data": serializer.data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberDetail(APIView):
    """
    Member Detailed Operations
    * Only staff users are able to access this view.
    """
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Member, pk=pk)

    def get(self, request, pk):
        """
        Returns list of all members
        """
        member = self.get_object(pk)
        return Response(MemberSerializer(member).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates provided member by pk
        """
        member = self.get_object(pk)
        serializer = MemberUpdateSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Member updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies provided member by pk
        """
        member = self.get_object(pk)
        serializer = MemberUpdateSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Member patched successfully.",
                "data": serializer.data,
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
