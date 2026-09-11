from django.conf import settings
from django.db import models
from django.utils import timezone

class Instrument(models.Model):
    class InstrumentType(models.TextChoices):
        WEIGHING_SCALE = "WEIGHING_SCALE", "Weighing Scale"
        ELECTRONIC_BALANCE = "ELECTRONIC_BALANCE", "Electronic Balance"
        PLATFORM_SCALE = "PLATFORM_SCALE", "Platform Scale"
        FUEL_DISPENSER = "FUEL_DISPENSER", "Fuel Dispenser"
        WATER_METER = "WATER_METER", "Water Meter"
        MEASURING_INSTRUMENT = "MEASURING_INSTRUMENT", "Measuring Instrument"
        OTHER = "OTHER", "Other"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instruments",
    )
    uid = models.CharField(max_length=32, unique=True, editable=False)
    name = models.CharField(max_length=255)
    instrument_type = models.CharField(max_length=40, choices=InstrumentType.choices)
    manufacturer = models.CharField(max_length=255)
    model_number = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, unique=True)
    capacity_range = models.CharField(max_length=255, blank=True)
    unit_of_measurement = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=500)
    installation_date = models.DateField(null=True, blank=True)
    qr_code = models.ImageField(upload_to="qr_codes/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.uid:
            year = timezone.now().year
            last = Instrument.objects.filter(uid__startswith=f"LM-INST-{year}-").order_by("-id").first()
            number = 1
            if last:
                try:
                    number = int(last.uid.rsplit("-", 1)[-1]) + 1
                except ValueError:
                    pass
            self.uid = f"LM-INST-{year}-{number:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.uid} - {self.name}"
