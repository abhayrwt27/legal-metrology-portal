from django.conf import settings
from django.db import models

class Document(models.Model):
    class DocumentType(models.TextChoices):
        APPLICATION = "APPLICATION", "Application Document"
        INSPECTION = "INSPECTION", "Inspection Document"
        SUPPORTING = "SUPPORTING", "Supporting Document"

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploaded_documents",
    )
    application = models.ForeignKey(
        "verification.VerificationApplication",
        on_delete=models.CASCADE,
        related_name="documents",
    )
    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
