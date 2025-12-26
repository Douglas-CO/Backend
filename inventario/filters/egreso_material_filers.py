from inventario.models.egreso_material_models import EgresoMaterial


class EgresoMaterialfilter:
    @staticmethod
    def filter_id(id: int):
        return EgresoMaterial.objects.filter(id=id)

    @staticmethod
    def filter_name(name: str):
        return EgresoMaterial.objects.filter(name__icontains=name)
    
    @staticmethod
    def filter_type(type: str):
        return EgresoMaterial.objects.filter(type=type)
    
    @staticmethod
    def filter_description(description: str):
        return EgresoMaterial.objects.filter(description__icontains=description)
    
    @staticmethod
    def filter_state(state: bool):
        return EgresoMaterial.objects.filter(state=state)