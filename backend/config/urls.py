from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/instruments/", include("instruments.urls")),
    path("api/verification/", include("verification.urls")),
    path("api/certificates/", include("certificates.urls")),
    path("api/documents/", include("documents.urls")),
    path("api/public/", include("verification.public_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
