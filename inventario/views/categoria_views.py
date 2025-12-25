from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework import status
from drf_yasg import openapi

from config.views.pagination import StandardResultsSetPagination
from inventario.models.categoria_models import Categoria
from inventario.services.categoria_services import CategoriaService
from inventario.serializers.categoria_serializers import CategoriaSerializer
from config.permissions.token_required import TokenRequiredPermission


class CategoriaListCreateView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Lista todos las categorias con paginación y filtros",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY,
                              description="Número de página", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              description="Cantidad por página", type=openapi.TYPE_INTEGER),
            openapi.Parameter('name', openapi.IN_QUERY,
                              description="Filtra por nombre", type=openapi.TYPE_STRING),
            openapi.Parameter('code', openapi.IN_QUERY,
                              description="Filtra por código", type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_QUERY,
                              description="Filtra por descripción", type=openapi.TYPE_STRING),
            openapi.Parameter('state', openapi.IN_QUERY,
                              description="Filtra por estado", type=openapi.TYPE_STRING),
        ],
        responses={200: CategoriaSerializer(many=True)}
    )
    def get(self, request):
        categorias_list = cache.get("categorias_list")
        if categorias_list is None:
            categorias_list = Categoria.objects.all()
            cache.set("categorias_list", categorias_list, timeout=60*5)

        categorias_qs = categorias_list

        # Filtros
        name = request.GET.get('name')
        code = request.GET.get('code')
        description = request.GET.get('description')
        state = request.GET.get('state')

        if name:
            categorias_qs = categorias_qs.filter(name__icontains=name)
        if code:
            categorias_qs = categorias_qs.filter(code__icontains=code)
        if description:
            categorias_qs = categorias_qs.filter(description__icontains=description)
        if state:
            if state.lower() in ['true', '1']:
                state_bool = True
            elif state.lower() in ['false', '0']:
                state_bool = False
            else:
                state_bool = None
            if state_bool is not None:
                categorias_qs = categorias_qs.filter(state=state_bool)

        # Paginación
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(categorias_qs, request)
        serializer = CategoriaSerializer(page, many=True)

        # Meta información
        total_count = categorias_qs.count()
        total_pages = (total_count // paginator.get_page_size(request)) + \
                      (1 if total_count % paginator.get_page_size(request) else 0)

        response_data = {
            "status": 200,
            "message": "Elementos paginados correctamente",
            "data": {
                "meta": {
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "count": total_count,
                    "total_pages": total_pages
                },
                "items": serializer.data
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Crea un nuevo categoria",
        request_body=CategoriaSerializer,
        responses={201: CategoriaSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        categoria = CategoriaService.crear_categoria(request.data)
        cache.delete("categorias_list")
        return Response({
            "status": 201,
            "message": "Categoria creado correctamente",
            "data": categoria
        }, status=status.HTTP_201_CREATED)


class CategoriaDetailView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Obtener categoria por UUID",
        responses={200: CategoriaSerializer, 404: "Not Found"}
    )
    def get(self, request, uuid):
        categoria = CategoriaService.obtener_categoria(uuid)
        if not categoria:
            return Response({"status": 404, "message": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": 200, "message": "Categoria obtenido correctamente", "data": categoria}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Actualizar categoria por UUID",
        request_body=CategoriaSerializer,
        responses={200: CategoriaSerializer,
                   400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, uuid):
        categoria = CategoriaService.actualizar_categoria(uuid, request.data)
        if not categoria:
            return Response({"status": 404, "message": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        cache.delete("categorias_list")
        return Response({"status": 200, "message": "Categoria actualizado correctamente", "data": categoria}, status=status.HTTP_200_OK)
