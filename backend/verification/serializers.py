from rest_framework import serializers
from .models import Inspection, VerificationApplication
from accounts.models import User

class InspectionSerializer(serializers.ModelSerializer):
    inspector_name = serializers.CharField(source="inspector.get_full_name", read_only=True)

    class Meta:
        model = Inspection
        fields = [
            "id", "application", "inspector", "inspector_name",
            "inspection_date", "inspection_location", "test_result",
            "measurements", "result", "remarks", "created_at"
        ]
        read_only_fields = ["id", "inspector", "inspector_name", "created_at"]

class ApplicationSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)
    instrument_uid = serializers.CharField(source="instrument.uid", read_only=True)
    instrument_name = serializers.CharField(source="instrument.name", read_only=True)
    assigned_gatc_name = serializers.CharField(source="assigned_gatc.get_full_name", read_only=True)
    inspection = InspectionSerializer(read_only=True)

    class Meta:
        model = VerificationApplication
        fields = [
            "id", "application_id", "owner", "owner_name",
            "instrument", "instrument_uid", "instrument_name",
            "application_type", "submission_date", "status",
            "assigned_gatc", "assigned_gatc_name",
            "lmo_remarks", "rejection_reason",
            "inspection", "created_at", "updated_at"
        ]
        read_only_fields = [
            "id", "application_id", "owner", "owner_name",
            "instrument_uid", "instrument_name", "submission_date",
            "status", "assigned_gatc_name", "lmo_remarks",
            "rejection_reason", "inspection", "created_at", "updated_at"
        ]

    def validate_instrument(self, instrument):
        request = self.context["request"]
        if request.user.is_owner and instrument.owner_id != request.user.id:
            raise serializers.ValidationError("You can only apply for your own instruments.")
        return instrument
