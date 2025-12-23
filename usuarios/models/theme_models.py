import uuid
from django.db import models
from config.models.AuditDateModel import AuditDateModel


class Theme(AuditDateModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    state = models.BooleanField(default=True)
    palette = models.JSONField()

    def __str__(self):
        return f"{self.name} ({self.code})"
