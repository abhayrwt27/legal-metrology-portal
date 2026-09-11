from django.contrib import admin
from .models import Inspection, VerificationApplication

@admin.register(VerificationApplication)
class VerificationApplicationAdmin(admin.ModelAdmin):
    list_display = ("application_id", "instrument", "owner", "status", "assigned_gatc", "submission_date")
    search_fields = ("application_id", "instrument__uid", "owner__username")
    list_filter = ("status", "application_type")

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ("application", "inspector", "inspection_date", "result")
    list_filter = ("result",)
