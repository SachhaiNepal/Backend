import datetime

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member, MemberRole
from accounts.serializers.member_role import MemberRoleSerializer, MemberRoleListSerializer
from accounts.sub_models.member_branch import MemberBranch


class ListMemberRole(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Member, pk=pk)

    def get(self, request, pk):
        member = self.get_object(pk)
        roles = MemberRole.objects.filter(member=member)
        return Response(
            MemberRoleListSerializer(roles, many=True).data, status=status.HTTP_200_OK
        )

    def post(self, request, pk):
        request.data["member"] = pk
        serializer = MemberRoleSerializer(data=request.data)

        member_branch_id = request.data["member_branch"]
        from_date = datetime.datetime.strptime(request.data["from_date"], "%Y-%m-%d").date()

        member = get_object_or_404(Member, pk=pk)
        member_branch = get_object_or_404(MemberBranch, pk=member_branch_id)

        if member_branch.member != member:
            return Response({
                "detail": "Please assign member branch of the same member."
            }, status=status.HTTP_403_FORBIDDEN)

        if member_branch.date_of_membership > from_date:
            return Response({
                "non_field_errors": ["Role period should be within the date of membership."]
            }, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({ "success": True }, status=status.HTTP_201_CREATED)
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

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response(
            {"message": "Member role deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
