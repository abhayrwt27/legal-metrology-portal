from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Instrument
from .serializers import InstrumentSerializer
from .services import generate_instrument_qr

class InstrumentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        user = request.user
        if user.is_owner:
            return Instrument.objects.filter(owner=user)
        return Instrument.objects.all()

    def get(self, request):
        serializer = InstrumentSerializer(
            self.get_queryset(request),
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_owner and not request.user.is_portal_admin:
            return Response({"detail": "Only owners can register instruments."}, status=403)
        serializer = InstrumentSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        owner = request.user if request.user.is_owner else request.user
        instrument = serializer.save(owner=owner)
        generate_instrument_qr(instrument)
        return Response(
            InstrumentSerializer(instrument, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

class InstrumentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, uid):
        try:
            instrument = Instrument.objects.get(uid=uid)
        except Instrument.DoesNotExist:
            return None
        if request.user.is_owner and instrument.owner_id != request.user.id:
            return None
        return instrument

    def get(self, request, uid):
        instrument = self.get_object(request, uid)
        if not instrument:
            return Response({"detail": "Instrument not found."}, status=404)
        return Response(InstrumentSerializer(instrument, context={"request": request}).data)
