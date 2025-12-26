from django.core.cache import cache
from inventario.serializers.egreso_material_serializers import EgresoMaterialSerializer
from inventario.repository.egreso_material_repository import EgresoMaterialRepository


class EgresoMaterialService:

    @staticmethod
    def create_egreso_material(data: dict):
        serializer = EgresoMaterialSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        egreso_material = serializer.save()

        # Limpiar cache
        cache.delete("egreso_materials_list")
        cache.delete("productos_list")

        return EgresoMaterialSerializer(egreso_material).data

    @staticmethod
    def get_egreso_material_all():
        egreso_materials = EgresoMaterialRepository.get_all()
        return EgresoMaterialSerializer(egreso_materials, many=True).data

    @staticmethod
    def get_egreso_material(uuid_value):
        egreso_material = EgresoMaterialRepository.get_uuid(uuid_value)
        if not egreso_material:
            return None
        return EgresoMaterialSerializer(egreso_material).data