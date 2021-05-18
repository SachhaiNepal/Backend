from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member
from accounts.serializers.member import MemberSerializer, MemberPOSTSerializer


class ListMember(APIView):
    """
    List Members
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        """
        Return a list of all users.
        """
        members = Member.objects.all()
        return Response(
            MemberSerializer(members, many=True).data, status=status.HTTP_200_OK
        )

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
    permission_classes = [IsAdminUser]

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
        serializer = MemberPOSTSerializer(
            member, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Member updated successfully.", "data": serializer.data},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Modifies provided member by pk
        """
        member = self.get_object(pk)
        serializer = MemberPOSTSerializer(
            member, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Member patched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
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
