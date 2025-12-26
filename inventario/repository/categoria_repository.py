from django.core.cache import cache
from inventario.models.categoria_models import Categoria


class CategoriaRepository:
    @staticmethod
    def crear_categoria(name: str, code: str, description: str, state: bool) -> Categoria:
        categoria = Categoria(
            name=name,
            code=code,
            description=description,
            state=state,
        )
        categoria.save()
        cache.delete("categorias_list")
        return categoria

    @staticmethod
    def obtener_por_uuid(uuid):
        try:
            return Categoria.objects.get(uuid=uuid)
        except Categoria.DoesNotExist:
            return None

    @staticmethod
    def obtener_por_code(code):
        try:
            return Categoria.objects.get(code=code)
        except Categoria.DoesNotExist:
            return None

    @staticmethod
    def listar_todos():
        categorias = cache.get("categorias_list")
        if categorias is None:
            categorias = list(categorias.objects.all())
            cache.set("categorias_list", categorias, timeout=60*5)
        return categorias
