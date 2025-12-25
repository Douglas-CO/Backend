from inventario.models.categoria_models import Categoria


class Categoriafilter:
    @staticmethod
    def filter_id(id: int):
        return Categoria.objects.filter(id=id)

    @staticmethod
    def filter_name(name: str):
        return Categoria.objects.filter(name__icontains=name)
    
    @staticmethod
    def filter_code(code: str):
        return Categoria.objects.filter(code=code)
    
    @staticmethod
    def filter_description(description: str):
        return Categoria.objects.filter(description__icontains=description)
    
    @staticmethod
    def filter_state(state: bool):
        return Categoria.objects.filter(state=state)