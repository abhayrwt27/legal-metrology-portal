from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Certificate
from .serializers import CertificateSerializer

class CertificateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        certificates = Certificate.objects.select_related("instrument", "instrument__owner")
        if request.user.is_owner:
            certificates = certificates.filter(instrument__owner=request.user)
        elif request.user.is_gatc:
            certificates = certificates.filter(application__assigned_gatc=request.user)
        return Response(CertificateSerializer(certificates, many=True).data)

class ExpiryMonitoringView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_owner:
            qs = Certificate.objects.filter(instrument__owner=request.user)
        elif request.user.is_lmo or request.user.is_portal_admin:
            qs = Certificate.objects.all()
        else:
            return Response({"detail": "You do not have permission to view expiry monitoring."}, status=403)

        today = timezone.localdate()
        soon = today + timezone.timedelta(days=30)
        expired = qs.filter(expiry_date__lt=today)
        expiring = qs.filter(expiry_date__gte=today, expiry_date__lte=soon)
        active = qs.filter(expiry_date__gt=soon, status=Certificate.Status.ACTIVE)

        return Response({
            "expired": CertificateSerializer(expired, many=True).data,
            "expiring_within_30_days": CertificateSerializer(expiring, many=True).data,
            "active": CertificateSerializer(active, many=True).data,
        })
