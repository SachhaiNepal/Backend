from rest_framework import serializers

from location.models import Country, VDCWard, VDC, MunicipalityWard, Municipality, District, Province


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = "__all__"


class MunicipalityWardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MunicipalityWard
        fields = "__all__"


class VDCSerializer(serializers.ModelSerializer):
    class Meta:
        model = VDC
        fields = "__all__"


class VDCWardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VDCWard
        fields = "__all__"
