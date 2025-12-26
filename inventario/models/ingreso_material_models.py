from django.db import models
import uuid

from inventario.models.producto_models import Producto
from config.models.AuditDateModel import AuditDateModel
from config.choices.inventario_choices import TYPE_CHOICES, SISTEMA

class IngresoMaterial(AuditDateModel):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=SISTEMA
    )
    description = models.CharField(max_length=255)
    state = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.type})"
    
class IngresoMaterialDetalle(models.Model):

    ingreso = models.ForeignKey(
        IngresoMaterial,
        on_delete=models.CASCADE,
        related_name='productos'
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )

    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.ingreso.name} - {self.producto.name} ({self.cantidad})"
