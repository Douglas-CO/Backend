from django.core.cache import cache
from venta.models.solicitud_servicio_models import SolicitudServicio


class SolicitudServicioRepository:

    @staticmethod
    def create_solicitud_servicio(**kwargs) -> SolicitudServicio:
        solicitud_servicio = SolicitudServicio.objects.create(**kwargs)
        cache.delete("solicitud_servicios_list")
        return solicitud_servicio

    @staticmethod
    def get_uuid(uuid):
        try:
            return SolicitudServicio.objects.get(uuid=uuid)
        except SolicitudServicio.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        solicitud_servicios = cache.get("solicitud_servicios_list")
        if solicitud_servicios is None:
            solicitud_servicios = list(SolicitudServicio.objects.all().order_by('-created_at'))
            cache.set("solicitud_servicios_list", solicitud_servicios, timeout=60*5)
        return solicitud_servicios

    @staticmethod
    def upd_solicitud_servicio(solicitud_servicio: SolicitudServicio, **kwargs):
        for key, value in kwargs.items():
            setattr(solicitud_servicio, key, value)
        solicitud_servicio.save()
        cache.delete("solicitud_servicios_list")
        return solicitud_servicio
