from django.urls import path
from rest_framework.routers import DefaultRouter

from event.views.event import (EventBannerImageViewSet, EventViewSet,
                               ToggleEventApprovalView)
from event.views.event_action import (EventCommentViewSet,
                                      EventInterestViewSet, EventStatistics,
                                      ToggleEventGoingStatus,
                                      ToggleEventInterestedStatus)
from event.views.event_media import (AddEventPhotoListView,
                                     AddEventVideoListView,
                                     AddEventVideoUrlsListView,
                                     EventPhotoViewSet, EventVideoUrlsViewSet,
                                     EventVideoViewSet)

router = DefaultRouter()
router.register(r"event", EventViewSet, basename="event")
router.register(r"event-banner", EventBannerImageViewSet, basename="event-banner")
router.register(r"event-image", EventPhotoViewSet, basename="event-image")
router.register(r"event-video", EventVideoViewSet, basename="event-video")
router.register(r"event-video-url", EventVideoUrlsViewSet, basename="event-video-url")
router.register(r"event-interest", EventInterestViewSet, basename="event-interest")
router.register(r"event-comment", EventCommentViewSet, basename="event-comment")
urlpatterns = router.urls

urlpatterns += [
    path("event/<int:pk>/approve", ToggleEventApprovalView.as_view()),
    path("event/<int:pk>/toggle-interested", ToggleEventInterestedStatus.as_view()),
    path("event/<int:pk>/toggle-going", ToggleEventGoingStatus.as_view()),
    path("event/<int:pk>/interest-statistics", EventStatistics.as_view()),
    path("event/<int:pk>/image-list", AddEventPhotoListView.as_view()),
    path("event/<int:pk>/video-url-list", AddEventVideoUrlsListView.as_view()),
    path("event/<int:pk>/video-list", AddEventVideoListView.as_view()),
]
