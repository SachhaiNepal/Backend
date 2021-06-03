from django.utils import timezone
from rest_framework import filters, generics, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly,
                                        IsAdminUser, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member, MemberBranch
from accounts.permissions import CanApproveMember
from accounts.serializers.member import MemberPOSTSerializer, MemberSerializer
from accounts.sub_models.member_role import MemberRole


class MemberFilterView(generics.ListAPIView):
    """
    Gets all the users in the database
    """

    queryset = Member.objects.all().order_by("-created_at")
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    filterset_fields = ["is_staff"]


class ListMember(APIView):
    """
    List Members
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser, DjangoModelPermissionsOrAnonReadOnly]

    @staticmethod
    def get_queryset():
        return Member.objects.all()

    @staticmethod
    def post(request):
        """
        Creates a brand member(x)
        """
        serializer = MemberPOSTSerializer(
            data=request.data, context={"request": request}
        )

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
    permission_classes = [IsAdminUser, DjangoModelPermissions]

    queryset = Member.objects.all()

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Member, pk=pk)

    def get(self, request, pk):
        """
        Returns list of all members
        """
        member = self.get_object(pk)
        return Response(MemberSerializer(member).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        member = self.get_object(pk)
        member_roles = MemberRole.objects.filter(member=member)
        member_branches = MemberBranch.objects.filter(member=member)
        [member_role.delete() for member_role in member_roles]
        [member_branch.delete() for member_branch in member_branches]
        member.delete()
        return Response(
            {
                "success": True,
            },
            status=status.HTTP_200_OK,
        )


class ToggleMemberApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, CanApproveMember]

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
            return Response(
                {
                    "message": "Member {} successfully.".format(
                        "approved" if member.is_approved else "rejected"
                    )
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        except Member.DoesNotExist:
            return Response(
                {"detail": "Member does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
