from rest_framework.routers import DefaultRouter

from utilities.views import (
    AboutUsImageViewSet,
    AboutUsViewSet,
    ServiceViewSet,
    ShowcaseGalleryViewSet,
    ShowcaseSliderViewSet,
)

router = DefaultRouter()
router.register(r"showcase-slider", ShowcaseSliderViewSet, basename="showcase-slider")
router.register(
    r"showcase-gallery", ShowcaseGalleryViewSet, basename="showcase-gallery"
)
router.register(r"service", ServiceViewSet, basename="service")
router.register(r"about-us", AboutUsViewSet, basename="about-us")
router.register(r"about-us-image", AboutUsImageViewSet, basename="about-us-image")

urlpatterns = router.urls
