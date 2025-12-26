from django.core.cache import cache
from inventario.models.egreso_material_models import EgresoMaterial 

class EgresoMaterialRepository:

    @staticmethod
    def create_egreso_material(
        name: str,
        type: str,
        description: str,
        state: bool
    ) -> EgresoMaterial:

        egreso_material = EgresoMaterial(
            name=name,
            type=type,
            description=description,
            state=state,
        )
        egreso_material.save()

        # Limpiar cache
        cache.delete("productos_list")
        cache.delete("egreso_materials_list")
        return egreso_material

    @staticmethod
    def get_uuid(uuid):
        try:
            return EgresoMaterial.objects.get(uuid=uuid)
        except EgresoMaterial.DoesNotExist:
            return None

    @staticmethod
    def get_all():
        egreso_materials = cache.get("egreso_materials_list")
        if egreso_materials is None:
            egreso_materials = list(EgresoMaterial.objects.all())
            cache.set("egreso_materials_list", egreso_materials, timeout=60 * 5)
        return egreso_materials
