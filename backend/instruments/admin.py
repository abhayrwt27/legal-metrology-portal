from django.contrib import admin
from .models import Instrument

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "instrument_type", "serial_number", "owner", "location")
    search_fields = ("uid", "name", "serial_number", "manufacturer")
    list_filter = ("instrument_type",)
