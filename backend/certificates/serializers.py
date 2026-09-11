from rest_framework import serializers
from .models import Certificate

class CertificateSerializer(serializers.ModelSerializer):
    instrument_uid = serializers.CharField(source="instrument.uid", read_only=True)
    instrument_name = serializers.CharField(source="instrument.name", read_only=True)
    is_valid = serializers.BooleanField(read_only=True)

    class Meta:
        model = Certificate
        fields = [
            "id", "number", "instrument_uid", "instrument_name",
            "issue_date", "expiry_date", "status",
            "verification_details", "is_valid", "created_at"
        ]
        read_only_fields = fields
