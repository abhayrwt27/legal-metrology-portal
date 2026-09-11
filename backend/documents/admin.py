from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "document_type", "application", "uploaded_by", "uploaded_at")
    search_fields = ("title", "application__application_id")
    list_filter = ("document_type",)
