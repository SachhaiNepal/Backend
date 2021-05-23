from django.urls import path
from rest_framework.routers import DefaultRouter

from event.views.event import EventViewSet, ToggleEventApprovalView

from event.views.event_media import EventPhotoViewSet, EventVideoUrlsViewSet


router = DefaultRouter()
router.register(r"event", EventViewSet, basename="event")
router.register(r"event-image", EventPhotoViewSet, basename="event-image")
router.register(r"event-video-url", EventVideoUrlsViewSet, basename="event-video-url")
urlpatterns = router.urls

urlpatterns += [
    path("event/<int:pk>/toggle-approval", ToggleEventApprovalView.as_view()),
]
