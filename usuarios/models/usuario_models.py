import uuid
from django.db import models
from config.models.AuditDateModel import AuditDateModel


class Usuario(AuditDateModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=10, unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.nombre} ({self.username})"
