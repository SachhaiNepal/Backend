from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member, MemberBranch, MemberRole, Profile
from accounts.serializers import (MemberBranchSerializer, MemberPOSTSerializer,
                                  MemberRoleSerializer, MemberSerializer,
                                  ProfilePOSTSerializer, ProfileSerializer,
                                  UserCreateSerializer, UserUpdateSerializer, RegisterFollowerSerializer)


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
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(get_user_model(), pk=pk)

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
                "data"   : UserCreateSerializer(self.get_object(pk)).data
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
                "data"   : UserCreateSerializer(self.get_object(pk)).data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response({
            "message": "User deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class ListMember(APIView):
    """
    List Members
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request):
        """
        Return a list of all users.
        """
        members = Member.objects.all()
        return Response(MemberSerializer(members, many=True).data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        """
        Creates a brand member(x)
        """
        serializer = MemberPOSTSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberDetail(APIView):
    """
    Member Detailed Operations
    * Only staff users are able to access this view.
    """
    authentication_classes = [TokenAuthentication]
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
        serializer = MemberPOSTSerializer(member, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Member updated successfully.",
                "data"   : serializer.data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies provided member by pk
        """
        member = self.get_object(pk)
        serializer = MemberPOSTSerializer(member, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Member patched successfully.",
                "data"   : serializer.data,
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToggleMemberApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            member = Member.objects.get(pk=pk)
            member.is_approved = not member.is_approved
            if member.is_approved:
                member.approved_by = request.user
                member.approved_at = timezone.now()
            else:
                member.approved_by = None
                member.approved_at = None
            member.save()
            return Response({
                "message": "Member {} successfully.".format("approved" if member.is_approved else "rejected")
            }, status=status.HTTP_204_NO_CONTENT)
        except Member.DoesNotExist:
            return Response({
                "detail": "Member does not exist."
            }, status=status.HTTP_404_NOT_FOUND)


class ListProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        """
        Return a profile of a user
        """
        user = get_object_or_404(get_user_model(), pk=pk)
        profile = Profile.objects.get(user=user)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)


class ProfileDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk):
        """
        Returns particular profile
        """
        profile = self.get_object(pk)
        return Response(ProfileSerializer(profile).data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Updates provided member by pk
        """
        profile = self.get_object(pk)
        serializer = ProfilePOSTSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully.",
                "data"   : ProfileSerializer(self.get_object(pk)).data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies provided member by pk
        """
        profile = self.get_object(pk)
        serializer = ProfilePOSTSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile patched successfully.",
                "data"   : ProfileSerializer(self.get_object(pk)).data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMemberRole(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Member, pk=pk)

    def get(self, request, pk):
        member = self.get_object(pk)
        roles = MemberRole.objects.filter(member=member)
        return Response(MemberRoleSerializer(roles, many=True).data, status=status.HTTP_200_OK)


class AddMemberRole(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MemberRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Member role added successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberRoleDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(MemberRole, pk=pk)

    def get(self, request, pk):
        role = self.get_object(pk)
        return Response(MemberRoleSerializer(role), status=status.HTTP_200_OK)

    def put(self, request, pk):
        role = self.get_object(pk)
        serializer = MemberRoleSerializer(role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Member role updated successfully.",
                "data": MemberRoleSerializer(self.get_object(pk)).data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response({
            "message": "Member role deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class ListMemberBranch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Member, pk=pk)

    def get(self, request, pk):
        member = self.get_object(pk)
        roles = MemberBranch.objects.filter(member=member)
        return Response(
            MemberBranchSerializer(roles, many=True).data,
            status=status.HTTP_200_OK)


class AddMemberBranch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MemberBranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Member branch added successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberBranchDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(MemberBranch, pk=pk)

    def get(self, request, pk):
        member_branch = self.get_object(pk)
        return Response(MemberBranchSerializer(member_branch), status=status.HTTP_200_OK)

    def put(self, request, pk):
        member_branch = self.get_object(pk)
        serializer = MemberBranchSerializer(member_branch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Member branch updated successfully.",
                "data": MemberBranchSerializer(self.get_object(pk)).data
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response({
            "message": "Member branch deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)


class RegisterFollower(APIView):

    @staticmethod
    def post(request):
        serializer = RegisterFollowerSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "message": "Follower registered successfully.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
