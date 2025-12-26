import uuid
from django.db import models
from django.core.validators import EmailValidator, RegexValidator

from usuarios.models.usuario_models import Usuario
from config.models.AuditDateModel import AuditDateModel
from config.choices.venta_choices import SEX_CHOICES, STATUS_CHOICES

class SolicitudServicio(AuditDateModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nombre = models.CharField(max_length=150)
    identificacion = models.CharField(max_length=10)
    email = models.CharField(
        max_length=100,
        validators=[EmailValidator(message="Email inválido")]
    )
    celular = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Debe tener 10 dígitos")]
    )
    sexo = models.CharField(
        max_length=10,
        choices=SEX_CHOICES
    )
    coord = models.CharField(max_length=255)
    is_discapacitado = models.BooleanField(default=False)
    is_tercera_edad = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="usuarios"
    )

    def __str__(self):
        return f"{self.nombre} ({self.status})"
