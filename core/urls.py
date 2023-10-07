import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.views import APIView

admin.site.site_header = getattr(settings, "SITE_NAME", "Django")
admin.site.site_title = getattr(
    settings, "SITE_TITLE", "Django Administration"
)

urlpatterns = []

if os.path.exists(os.path.join(settings.BASE_DIR, "router", "urls.py")):
    urlpatterns.insert(0, path("api/", include("router.urls")))


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.insert(0, path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns.insert(1, path("admin/", admin.site.urls))
