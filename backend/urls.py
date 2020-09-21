"""
backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
Ref: https://docs.djangoproject.com/en/3.0/topics/http/urls/

Examples:
    Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.home, name='home')
    Class-based views
        1. Add an import:  from other_app.views import Home
        2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    Including another URLconf
        1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
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

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
