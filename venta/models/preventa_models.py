import uuid
from django.db import models

from usuarios.models.usuario_models import Usuario
from inventario.models.producto_models import Producto
from config.models.AuditDateModel import AuditDateModel
from config.choices.venta_choices import STATUS_CHOICES
from venta.models.solicitud_servicio_models import SolicitudServicio


class Preventa(AuditDateModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDIENTE"
    )

    solicitud_servicio = models.ForeignKey(
        SolicitudServicio,
        on_delete=models.PROTECT,
        related_name="preventas"
    )

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="usuarios"
    )
    
    def __str__(self):
        return f"Preventa {self.uuid}"


class PreventaDetalle(AuditDateModel):
    preventa = models.ForeignKey(
        Preventa,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT
    )

    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Detalle de Preventa"
        verbose_name_plural = "Detalles de Preventa"
        constraints = [
            models.UniqueConstraint(
                fields=['preventa', 'producto'],
                name='unique_producto_por_preventa'
            )
        ]

    def __str__(self):
        return f"{self.preventa.uuid} - Producto {self.producto_id}"
