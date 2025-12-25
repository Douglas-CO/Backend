from inventario.repository.producto_repository import ProductoRepository
from inventario.serializers.producto_serializers import ProductoSerializer


class ProductoService:
    @staticmethod
    def create_producto(data: dict):
        payload = data.copy()
        serializer = ProductoSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def get_productos():
        producto = ProductoRepository.get_all()
        return ProductoSerializer(producto, many=True).data

    @staticmethod
    def get_usuario(uuid):
        producto = ProductoRepository.get_uuid(uuid)
        if not producto:
            return None
        return ProductoSerializer(producto).data

    @staticmethod
    def upd_producto(uuid, data: dict):
        producto = ProductoRepository.upd_producto(uuid)
        if not producto:
            return None

        serializer = ProductoSerializer(producto, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
