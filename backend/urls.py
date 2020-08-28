"""
backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
Ref: https://docs.djangoproject.com/en/3.0/topics/http/urls/

Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from accounts.views.load_country_province_and_district import load_countries, load_provinces, load_districts_of_nepal

urlpatterns = [
    path("admin/", admin.site.urls),
    path("select2/", include("django_select2.urls")),
    url(r"^api-auth/", include("rest_framework.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("branch.urls")),
    path("load-countries", load_countries),
    path("load-provinces", load_provinces),
    path("load-districts", load_districts_of_nepal)
]
