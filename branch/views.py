from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member
from accounts.serializers import MemberSerializer
from branch.models import Branch
from branch.serializers import BranchSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    # permission_classes = [permissions.IsAdminUser]


class BranchMembers(APIView):
    @staticmethod
    def get(request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
            members = Member.objects.filter(branch=branch)
            serializer = MemberSerializer(members, many=True)
            return Response({
                "count": members.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Branch.DoesNotExist:
            return Response({
                "details": "Branch not found."
            }, status=status.HTTP_404_NOT_FOUND)
