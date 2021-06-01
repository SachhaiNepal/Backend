from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from branch.serializers import *


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by("-created_at")
    serializer_class = BranchSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    filterset_fields = [
        "country", "province", "district",
        "municipality", "municipality_ward",
        "vdc", "vdc_ward",
        "is_main", "is_approved",
        "approved_by", "created_by"
    ]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return BranchPOSTSerializer
        return super(BranchViewSet, self).get_serializer_class()


class ToggleBranchApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response(
                {"detail": "Branch does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        branch.is_approved = not branch.is_approved
        if branch.is_approved:
            branch.approved_by = request.user
            branch.approved_at = timezone.now()
        else:
            branch.approved_by = None
            branch.approved_at = None
        branch.save()
        return Response(
            {
                "success": True,
                "message": "Branch {} successfully.".format(
                    "approved" if branch.is_approved else "rejected"
                ),
            },
            status=status.HTTP_204_NO_CONTENT,
        )
