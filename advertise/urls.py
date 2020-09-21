from rest_framework.routers import DefaultRouter

from advertise.views import *


router = DefaultRouter()
router.register(r"advertise", AdFileViewSet, basename="advertise")

urlpatterns = router.urls
