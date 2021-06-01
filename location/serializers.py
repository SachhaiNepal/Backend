from rest_framework import serializers

from location.models import (VDC, Country, District, Municipality,
                             MunicipalityWard, Province, VDCWard)


class MunicipalityWardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MunicipalityWard
        fields = "__all__"


class MunicipalitySerializer(serializers.ModelSerializer):
    municipality_wards = MunicipalityWardSerializer(many=True, read_only=True)

    class Meta:
        model = Municipality
        fields = "__all__"
        depth = 1


class MunicipalityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = "__all__"


class VDCWardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VDCWard
        fields = "__all__"


class VDCSerializer(serializers.ModelSerializer):
    vdc_wards = VDCWardSerializer(many=True, read_only=True)

    class Meta:
        model = VDC
        fields = "__all__"
        depth = 1


class VDCPostSerializer(serializers.ModelSerializer):
    vdc_wards = VDCWardSerializer(many=True, read_only=True)

    class Meta:
        model = VDC
        fields = "__all__"


class DistrictPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    municipalities = MunicipalitySerializer(many=True, read_only=True)
    vdcs = VDCSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = "__all__"
        depth = 2


class ProvinceSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True, read_only=True)

    class Meta:
        model = Province
        fields = "__all__"
        depth = 1


class ProvincePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    provinces = ProvinceSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = "__all__"
        depth = 1


class CountryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

