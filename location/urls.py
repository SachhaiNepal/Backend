from location.views import load_countries, load_provinces, load_districts_of_nepal
from django.urls import path

urlpatterns = [
    path("countries", load_countries),
    path("provinces", load_provinces),
    path("districts", load_districts_of_nepal),
]
