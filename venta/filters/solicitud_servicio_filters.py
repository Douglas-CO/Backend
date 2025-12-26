from django.db.models import Q
from venta.models.solicitud_servicio_models import SolicitudServicio


class SolicitudServicioFilters:

    @staticmethod
    def filter_fields(solicitud_servicio_filters: dict = None, usuario_filters: dict = None):
        qs = SolicitudServicio.objects.all()

        if solicitud_servicio_filters:
            for k, v in solicitud_servicio_filters.items():
                qs = qs.filter(**{f"{k}__icontains": v})

        if usuario_filters:
            q_obj = Q()
            for k, v in usuario_filters.items():
                q_obj &= Q(**{f"usuario__{k}__icontains": v})
            qs = qs.filter(q_obj)

        return qs
