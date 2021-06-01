from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from location.models import Country, District, Province
from utils.constants import COUNTRIES, DISTRICTS, PROVINCES


class LoadCountriesView(APIView):
    @staticmethod
    def post(request):
        for key, value in COUNTRIES:
            country, created = Country.objects.get_or_create(name=value)
            if created:
                country.save()
        return Response({"success": True}, status=status.HTTP_200_OK)


class LoadProvincesView(APIView):
    @staticmethod
    def post(request):
        for country_name, province_name, province_number in PROVINCES:
            country = Country.objects.get(name=country_name)
            obj, created = Province.objects.get_or_create(
                name=province_name, number=province_number, country=country
            )
            if created:
                obj.save()
        return Response({"success": True}, status=status.HTTP_200_OK)


class LoadDistrictsView(APIView):
    @staticmethod
    def post(request):
        for province_number, district_name in DISTRICTS:
            province = Province.objects.get(number=province_number)
            obj, created = District.objects.get_or_create(
                name=district_name,
                province=province,
            )
            if created:
                obj.save()
        return Response({"success": True}, status=status.HTTP_200_OK)
