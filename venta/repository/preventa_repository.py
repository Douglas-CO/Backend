from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.db import transaction
from typing import List, Dict

from inventario.models.producto_models import Producto
from venta.models.preventa_models import Preventa, PreventaDetalle


class PreventaRepository:

    @staticmethod
    @transaction.atomic
    def create_preventa(
        solicitud_servicio_id: int,
        productos: List[Dict],
        status: str = "PENDIENTE"
    ) -> Preventa:

        # Validar productos existentes
        productos_ids = [p["producto"] for p in productos]

        existentes = set(
            Producto.objects.filter(id__in=productos_ids)
            .values_list("id", flat=True)
        )

        invalidos = set(productos_ids) - existentes
        if invalidos:
            raise ValidationError({
                "productos": f"Productos no existen: {list(invalidos)}"
            })

        # Crear preventa
        preventa = Preventa.objects.create(
            solicitud_servicio_id=solicitud_servicio_id,
            status=status
        )

        # Crear detalles
        PreventaDetalle.objects.bulk_create([
            PreventaDetalle(
                preventa=preventa,
                producto_id=p["producto"],
                cantidad=p["cantidad"]
            )
            for p in productos
        ])

        # Limpiar cache
        cache.delete("preventas_list")

        return preventa

    @staticmethod
    def get_uuid(uuid):
        try:
            return Preventa.objects.get(uuid=uuid)
        except Preventa.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        preventas = cache.get("preventas_list")
        if preventas is None:
            preventas = list(
                Preventa.objects
                .select_related("solicitud_servicio")
                .prefetch_related("detalles__producto")
                .order_by("-created_at")
            )
            cache.set("preventas_list", preventas, timeout=60 * 5)
        return preventas

    @staticmethod
    def upd_preventa(preventa: Preventa, **kwargs):
        for key, value in kwargs.items():
            setattr(preventa, key, value)
        preventa.save()
        cache.delete("preventas_list")
        return preventa
