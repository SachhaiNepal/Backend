from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser

from location import models, serializers


class CountryViewSet(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.CountrySerializer
        else:
            return serializers.CountryPostSerializer


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = models.Province.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["country"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.ProvinceSerializer
        else:
            return serializers.ProvincePostSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = models.District.objects.all().order_by("-created_at")
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["province"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.DistrictSerializer
        else:
            return serializers.DistrictPostSerializer


class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = models.Municipality.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["district"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.MunicipalitySerializer
        else:
            return serializers.MunicipalityPostSerializer


class MunicipalityWardViewSet(viewsets.ModelViewSet):
    queryset = models.MunicipalityWard.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = serializers.MunicipalityWardSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["municipality"]


class VDCViewSet(viewsets.ModelViewSet):
    queryset = models.VDC.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["district"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return serializers.VDCSerializer
        else:
            return serializers.VDCPostSerializer


class VDCWardViewSet(viewsets.ModelViewSet):
    queryset = models.VDCWard.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = serializers.VDCWardSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["vdc"]
