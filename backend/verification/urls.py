from django.urls import path
from .views import (
    ApplicationDetailView, ApplicationListCreateView,
    ApproveApplicationView, AssignGATCView, DashboardView,
    GATCUsersView, InspectionCreateView, RejectApplicationView,
)

urlpatterns = [
    path("applications/", ApplicationListCreateView.as_view(), name="application-list"),
    path("applications/<str:application_id>/", ApplicationDetailView.as_view(), name="application-detail"),
    path("applications/<str:application_id>/assign/", AssignGATCView.as_view(), name="application-assign"),
    path("applications/<str:application_id>/inspection/", InspectionCreateView.as_view(), name="application-inspection"),
    path("applications/<str:application_id>/approve/", ApproveApplicationView.as_view(), name="application-approve"),
    path("applications/<str:application_id>/reject/", RejectApplicationView.as_view(), name="application-reject"),
    path("gatc-users/", GATCUsersView.as_view(), name="gatc-users"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
