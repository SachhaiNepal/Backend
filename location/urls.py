from django.urls import path
from rest_framework.routers import DefaultRouter

from location.views.loader import *
from location.views.views import *

router = DefaultRouter()
router.register(r"country", viewset=CountryViewSet, basename="country")
router.register(r"province", viewset=ProvinceViewSet, basename="province")
router.register(r"district", viewset=DistrictViewSet, basename="district")
router.register(r"municipality", viewset=MunicipalityViewSet, basename="municipality")
router.register(
    r"municipality-ward", viewset=MunicipalityWardViewSet, basename="municipality-ward"
)
router.register(r"vdc", viewset=VDCViewSet, basename="vdc")
router.register(r"vdc-ward", viewset=VDCWardViewSet, basename="vdc-ward")

urlpatterns = router.urls

urlpatterns += [
    path("load-countries", LoadCountriesView.as_view()),
    path("load-provinces", LoadProvincesView.as_view()),
    path("load-districts", LoadDistrictsView.as_view()),
]
