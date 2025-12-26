from venta.repository.solicitud_servicio_repository import SolicitudServicioRepository
from venta.serializers.solicitud_servicio_serializers import SolicitudServicioSerializer


class SolicitudServicioService:

    @staticmethod
    def create_solicitud_servicio(data: dict):
        serializer = SolicitudServicioSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def get_solicitud_servicios():
        solicitud_servicios = SolicitudServicioRepository.get_all()
        return SolicitudServicioSerializer(solicitud_servicios, many=True).data

    @staticmethod
    def get_solicitud_servicio(uuid):
        solicitud_servicio = SolicitudServicioRepository.get_uuid(uuid)
        if not solicitud_servicio:
            return None
        return SolicitudServicioSerializer(solicitud_servicio).data

    @staticmethod
    def upd_solicitud_servicio(uuid, data: dict):
        solicitud_servicio = SolicitudServicioRepository.get_uuid(uuid)
        if not solicitud_servicio:
            return None

        serializer = SolicitudServicioSerializer(
            solicitud_servicio, data=data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
