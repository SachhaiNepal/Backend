from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from branch.models import Branch
from branch.serializers import BranchSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAdminUser]
