from django.core.cache import cache

from venta.serializers.preventa_serializers import PreventaSerializer
from venta.repository.preventa_repository import PreventaRepository


class PreventaService:

    @staticmethod
    def create_preventa(data: dict):

        serializer = PreventaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        preventa = PreventaRepository.create_preventa(
            solicitud_servicio_id=validated["solicitud_servicio"].id,
            productos=validated["productos"],
            status=validated.get("status", "PENDIENTE")
        )

        cache.delete("preventas_list")

        return PreventaSerializer(preventa).data

    @staticmethod
    def get_preventa_all():
        preventas = PreventaRepository.get_all()
        return PreventaSerializer(preventas, many=True).data

    @staticmethod
    def get_preventa(uuid_value):
        preventa = PreventaRepository.get_uuid(uuid_value)
        if not preventa:
            return None
        return PreventaSerializer(preventa).data

    @staticmethod
    def upd_preventa(uuid, data: dict):
        preventa = PreventaRepository.get_uuid(uuid)
        if not preventa:
            return None

        serializer = PreventaSerializer(
            preventa,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        cache.delete("preventas_list")

        return serializer.data
