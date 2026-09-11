from django.db import models
from django.utils import timezone

class Certificate(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        EXPIRED = "EXPIRED", "Expired"
        REVOKED = "REVOKED", "Revoked"

    number = models.CharField(max_length=40, unique=True, editable=False)
    instrument = models.ForeignKey(
        "instruments.Instrument",
        on_delete=models.PROTECT,
        related_name="certificates",
    )
    application = models.OneToOneField(
        "verification.VerificationApplication",
        on_delete=models.PROTECT,
        related_name="certificate",
    )
    issue_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    verification_details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-issue_date"]

    def save(self, *args, **kwargs):
        if not self.number:
            year = timezone.now().year
            last = Certificate.objects.filter(number__startswith=f"LMCERT-{year}-").order_by("-id").first()
            number = 1
            if last:
                try:
                    number = int(last.number.rsplit("-", 1)[-1]) + 1
                except ValueError:
                    pass
            self.number = f"LMCERT-{year}-{number:06d}"
        if self.status == self.Status.ACTIVE and self.expiry_date < timezone.localdate():
            self.status = self.Status.EXPIRED
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return self.status == self.Status.ACTIVE and self.expiry_date >= timezone.localdate()
