from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter

from ad_file.views import *


router = DefaultRouter()
router.register(r"advertise", AdFileViewSet, basename="advertise")

urlpatterns = router.urls
