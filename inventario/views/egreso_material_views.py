from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework import status
from drf_yasg import openapi

from config.views.pagination import StandardResultsSetPagination
from inventario.models.egreso_material_models import EgresoMaterial
from config.permissions.token_required import TokenRequiredPermission
from inventario.services.egreso_material_services import EgresoMaterialService
from inventario.serializers.egreso_material_serializers import EgresoMaterialSerializer


class EgresoMaterialListCreateView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Lista todos los egresos de materiales con paginación y filtros",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY,
                              description="Número de página", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              description="Cantidad por página", type=openapi.TYPE_INTEGER),
            openapi.Parameter('name', openapi.IN_QUERY,
                              description="Filtra por nombre", type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY,
                              description="Filtra por tipo", type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_QUERY,
                              description="Filtra por descripción", type=openapi.TYPE_STRING),
            openapi.Parameter('state', openapi.IN_QUERY,
                              description="Filtra por estado", type=openapi.TYPE_STRING),
        ],
        responses={200: EgresoMaterialSerializer(many=True)}
    )
    def get(self, request):
        egreso_materials_list = cache.get("egreso_materials_list")
        if egreso_materials_list is None:
            egreso_materials_list = EgresoMaterial.objects.all()
            cache.set("egreso_materials_list", egreso_materials_list, timeout=60 * 5)

        egreso_materials_qs = egreso_materials_list

        # Filtros (SIN CAMBIOS GRANDES)
        name = request.GET.get('name')
        type_value = request.GET.get('type')
        description = request.GET.get('description')
        state = request.GET.get('state')

        if name:
            egreso_materials_qs = egreso_materials_qs.filter(name__icontains=name)

        if type_value:
            egreso_materials_qs = egreso_materials_qs.filter(type=type_value)

        if description:
            egreso_materials_qs = egreso_materials_qs.filter(description__icontains=description)

        if state:
            if state.lower() in ['true', '1']:
                egreso_materials_qs = egreso_materials_qs.filter(state=True)
            elif state.lower() in ['false', '0']:
                egreso_materials_qs = egreso_materials_qs.filter(state=False)

        # Paginación
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(egreso_materials_qs, request)
        serializer = EgresoMaterialSerializer(page, many=True)

        total_count = egreso_materials_qs.count()
        page_size = paginator.get_page_size(request)
        total_pages = (total_count // page_size) + (1 if total_count % page_size else 0)

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
        operation_description="Crea un nuevo egreso material",
        request_body=EgresoMaterialSerializer,
        responses={201: EgresoMaterialSerializer}
    )
    def post(self, request):
        egreso_material = EgresoMaterialService.create_egreso_material(request.data)
        cache.delete("egreso_materials_list")
        cache.delete("productos_list")
        return Response({
            "status": 201,
            "message": "Egreso Material creado correctamente",
            "data": egreso_material
        }, status=status.HTTP_201_CREATED)


class EgresoMaterialDetailView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Obtener egreso material por UUID",
        responses={200: EgresoMaterialSerializer, 404: "Not Found"}
    )
    def get(self, request, uuid):
        egreso_material = EgresoMaterialService.get_egreso_material(uuid)
        if not egreso_material:
            return Response(
                {"status": 404, "message": "No encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "status": 200,
            "message": "Egreso Material obtenido correctamente",
            "data": egreso_material
        }, status=status.HTTP_200_OK)