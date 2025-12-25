from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache

from inventario.models.producto_models import Producto
from inventario.services.producto_services import ProductoService
from inventario.serializers.producto_serializers import ProductoSerializer
from config.permissions.token_required import TokenRequiredPermission
from config.views.pagination import StandardResultsSetPagination


class ProductoListCreateView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Lista productos con filtros y paginación",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('code', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('state', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('categoria', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductoSerializer(many=True)}
    )
    def get(self, request):
        qs = cache.get("productos_qs")

        if qs is None:
            qs = Producto.objects.select_related('categoria').all()
            cache.set("productos_qs", qs, timeout=60)

        # 🔎 Filtros seguros
        filters = {}

        if request.GET.get("name"):
            filters["name__icontains"] = request.GET["name"]

        if request.GET.get("code"):
            filters["code__icontains"] = request.GET["code"]

        if request.GET.get("state") is not None:
            filters["state"] = request.GET.get("state").lower() == "true"

        if request.GET.get("categoria"):
            filters["categoria_id"] = request.GET["categoria"]

        qs = qs.filter(**filters)

        # 📄 Paginación
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = ProductoSerializer(page, many=True)

        return paginator.get_paginated_response({
            "items": serializer.data
        })

    @swagger_auto_schema(
        operation_description="Crear producto",
        request_body=ProductoSerializer,
        responses={201: ProductoSerializer}
    )
    def post(self, request):
        producto = ProductoService.crear_producto(request.data)
        cache.delete("productos_qs")
        return Response(producto, status=status.HTTP_201_CREATED)


class ProductoDetailView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Obtener producto por UUID",
        responses={200: ProductoSerializer, 404: "Not Found"}
    )
    def get(self, request, uuid):
        producto = ProductoService.obtener_producto(uuid)
        if not producto:
            return Response(
                {"detail": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(producto, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Actualizar producto por UUID",
        request_body=ProductoSerializer,
        responses={200: ProductoSerializer}
    )
    def patch(self, request, uuid):
        producto = ProductoService.actualizar_producto(uuid, request.data)
        if not producto:
            return Response(
                {"detail": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        cache.delete("productos_qs")
        return Response(producto, status=status.HTTP_200_OK)
