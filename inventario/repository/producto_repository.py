from decimal import Decimal
from django.core.cache import cache
from inventario.models.producto_models import Producto


class ProductoRepository:

    @staticmethod
    def create_producto(
        name: str,
        code: str,
        description: str,
        state: bool,
        iva: int,
        stock: int,
        valor: Decimal,
        categoria_id: int
    ) -> Producto:
        producto = Producto(
            name=name,
            code=code,
            description=description,
            state=state,
            iva=iva,
            stock=stock,
            valor=valor,
            categoria_id=categoria_id
        )
        producto.save()
        cache.delete("productos_list")
        return producto
    
    @staticmethod
    def get_uuid(uuid):
        try:
            return Producto.objects.get(uuid=uuid)
        except Producto.DoesNotExist:
            return None
        
    @staticmethod
    def get_all():
        productos = cache.get("productos_list")
        if productos is None:
            productos = list(Producto.objects.all())
            cache.set("productos_list", productos, timeout=60*5)
        return productos
    
    @staticmethod
    def upd_producto(producto: Producto, **kwargs):
        for key, value in kwargs.items():
            setattr(producto, key, value)
        producto.save()
        cache.delete("productos_list")
        return producto