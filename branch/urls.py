from django.urls import path
from rest_framework.routers import DefaultRouter

from branch.views.filter import *
from branch.views.views import *

router = DefaultRouter()
router.register(r"branch", BranchViewSet, basename="branch")
router.register(r"branch-image", BranchImageViewSet, basename="branch-image")
urlpatterns = router.urls

urlpatterns += [
    path("branch/<int:pk>/member", ListBranchMembers.as_view(), name="branch-members"),
    path("branch/<int:pk>/approve", ToggleBranchApprovalView.as_view()),
    path(
        "municipality/<int:pk>/branch",
        ListMunicipalityBranches.as_view(),
        name="municipality-branches",
    ),
    path(
        "vdc/<int:pk>/branch", ListVdcBranches.as_view(), name="municipality-branches"
    ),
    path(
        "municipality-ward/<int:pk>/branch",
        ListMunicipalityWardBranch.as_view(),
        name="municipality-branches",
    ),
    path(
        "vdc-ward/<int:pk>/branch",
        ListVdcWardBranch.as_view(),
        name="municipality-branches",
    ),
]
