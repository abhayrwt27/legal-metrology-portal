from rest_framework import serializers
from .models import Instrument

class InstrumentSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Instrument
        fields = [
            "id", "uid", "name", "instrument_type", "manufacturer",
            "model_number", "serial_number", "capacity_range",
            "unit_of_measurement", "location", "installation_date",
            "qr_code_url", "owner_name", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "uid", "qr_code_url", "owner_name", "created_at", "updated_at"]

    def get_qr_code_url(self, obj):
        request = self.context.get("request")
        if obj.qr_code and request:
            return request.build_absolute_uri(obj.qr_code.url)
        return None
