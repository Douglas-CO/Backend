import uuid
from django.db import models

from config.models.AuditDateModel import AuditDateModel
from venta.models.solicitud_servicio_models import SolicitudServicio
from inventario.models.producto_models import Producto
from config.choices.venta_choices import STATUS_CHOICES


class Preventa(AuditDateModel):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDIENTE"  # Ajusta según tus STATUS_CHOICES
    )

    solicitud_servicio = models.ForeignKey(
        SolicitudServicio,
        on_delete=models.PROTECT,
        related_name="preventas"
    )

    class Meta:
        verbose_name = "Preventa"
        verbose_name_plural = "Preventas"
        ordering = ["-created_at"]

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
