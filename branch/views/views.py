from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from branch.serializers import *


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by("-created_at")
    serializer_class = BranchSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields = ["name"]
    filterset_fields = [
        "country",
        "province",
        "district",
        "municipality",
        "municipality_ward",
        "vdc",
        "vdc_ward",
        "is_main",
        "is_approved",
        "approved_by",
        "created_by",
    ]

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return BranchPOSTSerializer
        return super(BranchViewSet, self).get_serializer_class()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BranchPOSTSerializer(
            instance,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToggleBranchApprovalView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        if not branch.is_approved:
            branch.is_approved = True
            branch.approved_by = request.user
            branch.approved_at = timezone.now()
            branch.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def delete(request, pk):
        branch = get_object_or_404(Branch, pk=pk)
        if branch.is_approved:
            branch.is_approved = False
            branch.approved_by = None
            branch.approved_at = None
            branch.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BranchImageViewSet(viewsets.ModelViewSet):
    queryset = BranchImage.objects.all()
    serializer_class = BranchImageSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filterset_fields = ["branch"]

    def destroy(self, request, *args, **kwargs):
        branch_image = self.get_object()
        branch_image.image.delete()
        branch_image.delete()
        return Response(
            {"message": "Branch image deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )
