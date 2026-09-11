from django.urls import path
from .views_public import PublicInstrumentVerificationView

urlpatterns = [
    path("verify/<str:uid>/", PublicInstrumentVerificationView.as_view(), name="public-verify"),
]
