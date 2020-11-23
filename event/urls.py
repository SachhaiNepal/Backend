from django.urls import path
from rest_framework.routers import DefaultRouter

from event.filter import *
from event.views import *

router = DefaultRouter()
router.register(r'event', EventViewSet, basename='event')
router.register(r'event-photo', EventPhotoViewSet, basename='event-photo')
router.register(r'event-video-url', EventVideoUrlsViewSet, basename='event-video-url')
urlpatterns = router.urls

urlpatterns += [
    path("event/<int:pk>/photo", ListEventPhotos.as_view()),
    path("event/<int:pk>/video-urls", ListEventVideoUrls.as_view()),
    path("event/<int:pk>/toggle-approval", ToggleEventApprovalView.as_view()),
]
