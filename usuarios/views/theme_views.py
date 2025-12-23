from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework import status
from drf_yasg import openapi

from usuarios.models.theme_models import Theme
from usuarios.services.theme_services import ThemeService
from usuarios.serializers.theme_serializers import ThemeSerializer
from config.permissions.token_required import TokenRequiredPermission


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ThemeListCreateView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Lista todos los themes con paginación y filtros",
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
        responses={200: ThemeSerializer(many=True)}
    )
    def get(self, request):
        # Obtener themes desde cache o base de datos
        themes_list = cache.get("themes_list")
        if themes_list is None:
            themes_list = Theme.objects.all()
            cache.set("themes_list", themes_list, timeout=60*5)

        themes_qs = themes_list

        # Filtros
        name = request.GET.get('name')
        code = request.GET.get('code')
        description = request.GET.get('description')
        state = request.GET.get('state')

        if name:
            themes_qs = themes_qs.filter(name__icontains=name)
        if code:
            themes_qs = themes_qs.filter(code__icontains=code)
        if description:
            themes_qs = themes_qs.filter(description__icontains=description)
        if state:
            if state.lower() in ['true', '1']:
                state_bool = True
            elif state.lower() in ['false', '0']:
                state_bool = False
            else:
                state_bool = None
            if state_bool is not None:
                themes_qs = themes_qs.filter(state=state_bool)

        # Paginación
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(themes_qs, request)
        serializer = ThemeSerializer(page, many=True)

        # Meta información
        total_count = themes_qs.count()
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
        operation_description="Crea un nuevo theme",
        request_body=ThemeSerializer,
        responses={201: ThemeSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        theme = ThemeService.crear_theme(request.data)
        cache.delete("themes_list")
        return Response({
            "status": 201,
            "message": "Theme creado correctamente",
            "data": theme
        }, status=status.HTTP_201_CREATED)


class ThemeDetailView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Obtener theme por UUID",
        responses={200: ThemeSerializer, 404: "Not Found"}
    )
    def get(self, request, uuid):
        theme = ThemeService.obtener_theme(uuid)
        if not theme:
            return Response({"status": 404, "message": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": 200, "message": "Theme obtenido correctamente", "data": theme}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Actualizar theme por UUID",
        request_body=ThemeSerializer,
        responses={200: ThemeSerializer,
                   400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, uuid):
        theme = ThemeService.actualizar_theme(uuid, request.data)
        if not theme:
            return Response({"status": 404, "message": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        cache.delete("themes_list")
        return Response({"status": 200, "message": "Theme actualizado correctamente", "data": theme}, status=status.HTTP_200_OK)
