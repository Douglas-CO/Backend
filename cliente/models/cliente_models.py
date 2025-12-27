import uuid
from django.db import models
from config.models.AuditDateModel import AuditDateModel
from config.choices.venta_choices import SEX_CHOICES


class Cliente(AuditDateModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    identificacion = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=250)
    direccion = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=10, choices=SEX_CHOICES)

    is_discapacitado = models.BooleanField(default=False)
    is_tercera_edad = models.BooleanField(default=False)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.identificacion
