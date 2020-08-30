from django.urls import path
from rest_framework.routers import DefaultRouter

from branch.views import BranchViewSet, BranchMembers

router = DefaultRouter()
router.register(r'branch', BranchViewSet, basename='branch')
urlpatterns = router.urls
urlpatterns += [
    path("branch/<int:pk>/member", BranchMembers.as_view(), name="branch-members")
]
