from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from location import models, serializers


class CountryViewSet(viewsets.ModelViewSet):
    search_fields = ["name"]
    permission_classes = [IsAdminUser]
    queryset = models.Country.objects.all()
    filter_backends = [filters.SearchFilter]
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.CountrySerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    search_fields = ["name"]
    filterset_fields = ["country"]
    permission_classes = [IsAdminUser]
    queryset = models.Province.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.ProvinceSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = models.District.objects.all().order_by("-created_at")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    search_fields = ["name"]
    filterset_fields = ["province"]
    serializer_class = serializers.DistrictSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]


class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = models.Municipality.objects.all()
    search_fields = ["name"]
    filterset_fields = ["district"]
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.MunicipalitySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]


class MunicipalityWardViewSet(viewsets.ModelViewSet):
    search_fields = ["name"]
    permission_classes = [IsAdminUser]
    filterset_fields = ["municipality"]
    authentication_classes = [TokenAuthentication]
    queryset = models.MunicipalityWard.objects.all()
    serializer_class = serializers.MunicipalityWardSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]


class VDCViewSet(viewsets.ModelViewSet):
    search_fields = ["name"]
    filterset_fields = ["district"]
    permission_classes = [IsAdminUser]
    queryset = models.VDC.objects.all()
    serializer_class = serializers.VDCSerializer
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]


class VDCWardViewSet(viewsets.ModelViewSet):
    search_fields = ["name"]
    filterset_fields = ["vdc"]
    permission_classes = [IsAdminUser]
    queryset = models.VDCWard.objects.all()
    authentication_classes = [TokenAuthentication]
    serializer_class = serializers.VDCWardSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
