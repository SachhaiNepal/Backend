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


class ListBranchMembers(APIView):
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


# ------------> Filter APIs Below <-------------

class ListMunicipalityBranches(APIView):
    @staticmethod
    def get(request, pk):
        try:
            municipality = Municipality.objects.get(pk=pk)
            branches = Branch.objects.filter(municipality=municipality)
            serializer = BranchSerializer(branches, many=True)
            return Response({
                "count": branches.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Municipality.DoesNotExist:
            return Response({
                "details": "Municipality not found."
            }, status=status.HTTP_404_NOT_FOUND)


class ListVdcBranches(APIView):
    @staticmethod
    def get(request, pk):
        try:
            vdc = VDC.objects.get(pk=pk)
            branches = Branch.objects.filter(branch=vdc)
            serializer = BranchSerializer(branches, many=True)
            return Response({
                "count": branches.count(),
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except VDC.DoesNotExist:
            return Response({
                "details": "VDC not found."
            }, status=status.HTTP_404_NOT_FOUND)


class ListMunicipalityWardBranch(APIView):
    @staticmethod
    def get(request, pk):
        try:
            municipality_ward = MunicipalityWard.objects.get(pk=pk)
            branch = Branch.objects.get(municipality_ward=municipality_ward)
            serializer = BranchSerializer(branch)
            return Response({
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Branch.DoesNotExist:
            return Response({
                "details": "Municipality Ward not found."
            }, status=status.HTTP_404_NOT_FOUND)


class ListVdcWardBranch(APIView):
    @staticmethod
    def get(request, pk):
        try:
            vdc_ward = VDCWard.objects.get(pk=pk)
            branch = Branch.objects.filter(vdc_ward=vdc_ward)
            serializer = MemberSerializer(branch)
            return Response({
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Branch.DoesNotExist:
            return Response({
                "details": "VDC Ward not found."
            }, status=status.HTTP_404_NOT_FOUND)
