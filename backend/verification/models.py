from django.conf import settings
from django.db import models
from django.utils import timezone

class VerificationApplication(models.Model):
    class ApplicationType(models.TextChoices):
        INITIAL = "INITIAL", "Initial Verification"
        REVERIFICATION = "REVERIFICATION", "Re-verification"
        RENEWAL = "RENEWAL", "Renewal"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        ASSIGNED = "ASSIGNED", "Assigned"
        INSPECTION_COMPLETED = "INSPECTION_COMPLETED", "Inspection Completed"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    application_id = models.CharField(max_length=40, unique=True, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    instrument = models.ForeignKey("instruments.Instrument", on_delete=models.PROTECT, related_name="applications")
    application_type = models.CharField(max_length=20, choices=ApplicationType.choices)
    submission_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.DRAFT)
    assigned_gatc = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_applications",
    )
    lmo_remarks = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.application_id:
            year = timezone.now().year
            last = VerificationApplication.objects.filter(
                application_id__startswith=f"LM-APP-{year}-"
            ).order_by("-id").first()
            number = 1
            if last:
                try:
                    number = int(last.application_id.rsplit("-", 1)[-1]) + 1
                except ValueError:
                    pass
            self.application_id = f"LM-APP-{year}-{number:06d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.application_id

class Inspection(models.Model):
    class Result(models.TextChoices):
        PASS = "PASS", "Pass"
        FAIL = "FAIL", "Fail"

    application = models.OneToOneField(
        VerificationApplication,
        on_delete=models.CASCADE,
        related_name="inspection",
    )
    inspector = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="inspections",
    )
    inspection_date = models.DateField()
    inspection_location = models.CharField(max_length=500)
    test_result = models.CharField(max_length=255)
    measurements = models.JSONField(default=dict, blank=True)
    result = models.CharField(max_length=4, choices=Result.choices)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
