from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member
from accounts.serializers import MemberSerializer
from branch.models import Branch
from branch.serializers import BranchSerializer
from location.models import Municipality, VDC, MunicipalityWard, VDCWard


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    # permission_classes = [permissions.IsAdminUser]
