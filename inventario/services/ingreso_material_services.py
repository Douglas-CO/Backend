from inventario.repository.ingreso_material_repository import IngresoMaterialRepository
from inventario.serializers.ingreso_material_serializers import IngresoMaterialSerializer


class IngresoMaterialService:

    @staticmethod
    def create_ingreso_material(data: dict):
        serializer = IngresoMaterialSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        ingreso_material = IngresoMaterialRepository.create_ingreso_material(
            name=serializer.validated_data["name"],
            type=serializer.validated_data["type"],
            description=serializer.validated_data.get("description", ""),
            state=serializer.validated_data.get("state", True),
        )

        return IngresoMaterialSerializer(ingreso_material).data

    @staticmethod
    def get_ingreso_material_all():
        ingreso_materials = IngresoMaterialRepository.get_all()
        return IngresoMaterialSerializer(ingreso_materials, many=True).data

    @staticmethod
    def get_ingreso_material(uuid_value):
        ingreso_material = IngresoMaterialRepository.get_uuid(uuid_value)
        if not ingreso_material:
            return None
        return IngresoMaterialSerializer(ingreso_material).data
