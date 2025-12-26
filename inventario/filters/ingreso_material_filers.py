from inventario.models.ingreso_material_models import IngresoMaterial


class IngresoMaterialfilter:
    @staticmethod
    def filter_id(id: int):
        return IngresoMaterial.objects.filter(id=id)

    @staticmethod
    def filter_name(name: str):
        return IngresoMaterial.objects.filter(name__icontains=name)
    
    @staticmethod
    def filter_type(type: str):
        return IngresoMaterial.objects.filter(type=type)
    
    @staticmethod
    def filter_description(description: str):
        return IngresoMaterial.objects.filter(description__icontains=description)
    
    @staticmethod
    def filter_state(state: bool):
        return IngresoMaterial.objects.filter(state=state)