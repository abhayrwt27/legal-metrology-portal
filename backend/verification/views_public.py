from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from certificates.models import Certificate
from instruments.models import Instrument

class PublicInstrumentVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid):
        try:
            instrument = Instrument.objects.get(uid=uid)
        except Instrument.DoesNotExist:
            return Response({"detail": "Instrument not found."}, status=404)

        today = timezone.localdate()
        certificates = instrument.certificates.all().order_by("-issue_date")
        current = certificates.filter(
            status=Certificate.Status.ACTIVE,
            expiry_date__gte=today,
        ).first()

        return Response({
            "instrument": {
                "uid": instrument.uid,
                "name": instrument.name,
                "instrument_type": instrument.get_instrument_type_display(),
                "manufacturer": instrument.manufacturer,
                "model_number": instrument.model_number,
                "serial_number": instrument.serial_number,
                "capacity_range": instrument.capacity_range,
                "unit_of_measurement": instrument.unit_of_measurement,
                "location": instrument.location,
            },
            "verification_status": "VALID" if current else "EXPIRED",
            "current_certificate": {
                "number": current.number,
                "status": current.status,
                "issue_date": current.issue_date,
                "expiry_date": current.expiry_date,
            } if current else None,
            "certificate_history": [
                {
                    "number": cert.number,
                    "status": cert.status,
                    "issue_date": cert.issue_date,
                    "expiry_date": cert.expiry_date,
                }
                for cert in certificates[:10]
            ],
        })
