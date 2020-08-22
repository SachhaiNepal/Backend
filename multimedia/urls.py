from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # to be added
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
