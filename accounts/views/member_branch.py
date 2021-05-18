from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member, MemberBranch
from accounts.serializers.member_branch import MemberBranchSerializer


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
            MemberBranchSerializer(roles, many=True).data, status=status.HTTP_200_OK
        )

    def post(self, request, pk):
        request.data["member"] = pk
        serializer = MemberBranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberBranchDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(MemberBranch, pk=pk)

    def get(self, request, pk):
        member_branch = self.get_object(pk)
        return Response(
            MemberBranchSerializer(member_branch), status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response(
            {"message": "Member branch deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
