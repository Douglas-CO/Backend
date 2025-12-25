from inventario.models.categoria_models import Categoria
from inventario.repository.categoria_repository import CategoriaRepository
from inventario.serializers.categoria_serializers import CategoriaSerializer

class CategoriaService:
    
    @staticmethod
    def crear_categoria(data: dict):
        serializer = CategoriaSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        categoria = serializer.save()
        return serializer.data

    @staticmethod
    def listar_categoria():
        categorias = CategoriaRepository.listar_todos()
        return CategoriaSerializer(categorias, many=True).data

    @staticmethod
    def obtener_categoria(uuid):
        categoria = CategoriaRepository.obtener_por_uuid(uuid)
        if not categoria:
            return None
        return CategoriaSerializer(categoria).data

    @staticmethod
    def actualizar_categoria(uuid, data: dict):
        categoria = CategoriaRepository.obtener_por_uuid(uuid)
        if not categoria:
            return None
        serializer = CategoriaSerializer(categoria, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        categoria = serializer.save()
        return serializer.data
