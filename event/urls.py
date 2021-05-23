from django.urls import path
from rest_framework.routers import DefaultRouter

from event.views.event import EventViewSet, ToggleEventApprovalView
from event.views.event_action import (EventCommentViewSet,
                                      EventInterestViewSet, EventStatistics)
from event.views.event_media import (EventPhotoViewSet, EventVideoUrlsViewSet,
                                     EventVideoViewSet)

router = DefaultRouter()
router.register(r"event", EventViewSet, basename="event")
router.register(r"event-image", EventPhotoViewSet, basename="event-image")
router.register(r"event-video", EventVideoViewSet, basename="event-video")
router.register(r"event-video-url", EventVideoUrlsViewSet, basename="event-video-url")
router.register(r"event-interest", EventInterestViewSet, basename="event-interest")
router.register(r"event-comment", EventCommentViewSet, basename="event-comment")
urlpatterns = router.urls

urlpatterns += [
    path("event/<int:pk>/toggle-approval", ToggleEventApprovalView.as_view()),
    path("event/<int:pk>/interest-statistics", EventStatistics.as_view()),
]
