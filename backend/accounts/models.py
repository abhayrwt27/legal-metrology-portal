from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        LMO = "LMO", "Legal Metrology Officer"
        GATC = "GATC", "Government Approved Test Centre"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=5, choices=Role.choices, default=Role.OWNER)
    phone_number = models.CharField(max_length=20, blank=True)
    organization_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_owner(self):
        return self.role == self.Role.OWNER

    @property
    def is_lmo(self):
        return self.role == self.Role.LMO

    @property
    def is_gatc(self):
        return self.role == self.Role.GATC

    @property
    def is_portal_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
