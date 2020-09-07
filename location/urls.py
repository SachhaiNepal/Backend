from rest_framework.routers import DefaultRouter

from location.views.loader import *
from location.views.views import *
from django.urls import path

router = DefaultRouter()
router.register(r"country", viewset=CountryViewSet, basename="country")
router.register(r"province", viewset=ProvinceViewSet, basename="province")
router.register(r"district", viewset=DistrictViewSet, basename="district")
router.register(r"municipality", viewset=MunicipalityViewSet, basename="municipality")
router.register(r"vdc", viewset=VDCViewSet, basename="vdc")

urlpatterns = router.urls

urlpatterns += [
    path("load-countries", load_countries),
    path("load-provinces", load_provinces_of_nepal),
    path("load-districts", load_districts_of_nepal),
    # TODO: yet to be implemented
    # path("municipality/<int:pk>/ward", ListMunicipalityWard.as_view()),
    # path("vdc/<int:pk>/ward", ListVdcWard.as_view())
]
