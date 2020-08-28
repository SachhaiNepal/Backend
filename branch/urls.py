from rest_framework.routers import DefaultRouter

from branch.views import BranchViewSet

router = DefaultRouter()
router.register(r'branch', BranchViewSet, basename='branch')
urlpatterns = router.urls
