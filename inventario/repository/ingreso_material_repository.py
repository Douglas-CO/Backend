from django.core.cache import cache
from inventario.models.ingreso_material_models import IngresoMaterial

class IngresoMaterialRepository:

    @staticmethod
    def create_ingreso_material(
        name: str,
        type: str,
        description: str,
        state: bool
    ) -> IngresoMaterial:

        ingreso_material = IngresoMaterial(
            name=name,
            type=type,
            description=description,
            state=state,
        )
        ingreso_material.save()

        cache.delete("productos_list")
        cache.delete("ingreso_materials_list")
        return ingreso_material

    @staticmethod
    def get_uuid(uuid):
        try:
            return IngresoMaterial.objects.get(uuid=uuid)
        except IngresoMaterial.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        ingreso_materials = cache.get("ingreso_materials_list")

        if ingreso_materials is None:
            ingreso_materials = list(IngresoMaterial.objects.all())
            cache.set("ingreso_materials_list", ingreso_materials, timeout=60 * 5)

        return ingreso_materials
