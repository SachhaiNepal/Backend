from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from location.models import Country, Province, District
from utils.constants import COUNTRIES, PROVINCES, DISTRICTS


@permission_required('accounts.countries.add_country', raise_exception=True)
def load_countries(request):
    for key, value in COUNTRIES:
        country, created = Country.objects.get_or_create(name=value)
        if created:
            country.save()
    return HttpResponse("<h4>Countries Added Successfully.</h4>")


@permission_required('accounts.countries.add_province', raise_exception=True)
def load_provinces_of_nepal(request):
    for country_name, province_name, province_number in PROVINCES:
        country = Country.objects.get(name=country_name)
        obj, created = Province.objects.get_or_create(
            name=province_name,
            number=province_number,
            country=country
        )
        if created:
            obj.save()
    return HttpResponse("<h4>Provinces Added Successfully.</h4>")


@permission_required('accounts.countries.add_district', raise_exception=True)
def load_districts_of_nepal(request):
    country = Country.objects.get(name="Nepal")
    for province_number, district_name in DISTRICTS:
        province = Province.objects.get(number=province_number)
        obj, created = District.objects.get_or_create(
            name=district_name,
            province=province,
            country=country
        )
        if created:
            obj.save()
    return HttpResponse("<h4>Districts Added Successfully.</h4>")
