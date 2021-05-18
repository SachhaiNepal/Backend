from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member, MemberRole
from accounts.serializers import MemberRoleSerializer


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
            MemberRoleSerializer(roles, many=True).data, status=status.HTTP_200_OK
        )


class CreateMemberRole(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MemberRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Member role added successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
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
            return Response(
                {
                    "message": "Member role updated successfully.",
                    "data": MemberRoleSerializer(self.get_object(pk)).data,
                },
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        role = self.get_object(pk)
        role.delete()
        return Response(
            {"message": "Member role deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
