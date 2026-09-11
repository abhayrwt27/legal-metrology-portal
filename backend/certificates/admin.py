from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("number", "instrument", "issue_date", "expiry_date", "status")
    search_fields = ("number", "instrument__uid")
    list_filter = ("status",)
