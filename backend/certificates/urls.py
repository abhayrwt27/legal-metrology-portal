from django.urls import path
from .views import CertificateListView, ExpiryMonitoringView

urlpatterns = [
    path("", CertificateListView.as_view(), name="certificate-list"),
    path("expiry/", ExpiryMonitoringView.as_view(), name="certificate-expiry"),
]
