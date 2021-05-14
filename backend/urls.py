from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("", admin.site.urls),
    path("select2/", include("django_select2.urls")),
    url(r"^api-auth/", include("rest_framework.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("branch.urls")),
    path("api/", include("multimedia.urls")),
    path("api/", include("location.urls")),
    path("api/", include("advertise.urls")),
    path("api/", include("event.urls")),
    path("api/", include("utilities.urls")),
    url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
