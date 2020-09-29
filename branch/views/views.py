from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Member
from accounts.serializers import MemberSerializer
from branch.models import Branch
from branch.serializers import BranchSerializer
from location.models import VDC, Municipality, MunicipalityWard, VDCWard


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    # permission_classes = [permissions.IsAdminUser]
