from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member, MemberBranch
from accounts.serializers.member_branch import (MemberBranchListSerializer,
                                                MemberBranchSerializer)


class ListMemberBranch(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_object(pk):
        return get_object_or_404(Member, pk=pk)

    def get(self, request, pk):
        member = self.get_object(pk)
        member_branches = MemberBranch.objects.filter(member=member)
        return Response(
            MemberBranchListSerializer(member_branches, many=True).data,
            status=status.HTTP_200_OK,
        )

    def post(self, request, pk):
        request.data["member"] = pk
        serializer = MemberBranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberBranchViewSet(viewsets.ModelViewSet):
    queryset = MemberBranch.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["member", "branch"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MemberBranchListSerializer
        else:
            return MemberBranchSerializer
