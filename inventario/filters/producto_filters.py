from django.db.models import Q
from inventario.models.producto_models import Producto


class ProductoFilters:

    @staticmethod
    def filter_fields(
        producto_filters: dict = None,
        categoria_filters: dict = None
    ):
        qs = Producto.objects.all()

        if producto_filters:
            qs = qs.filter(**producto_filters)

        if categoria_filters:
            q_obj = Q()
            for k, v in categoria_filters.items():
                q_obj &= Q(**{f"categoria__{k}__icontains": v})

            qs = qs.filter(q_obj)

        return qs