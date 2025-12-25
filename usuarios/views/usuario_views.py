from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

from usuarios.models.usuario_models import Usuario
from usuarios.services.usuario_services import UsuarioService
from config.permissions.token_required import TokenRequiredPermission
from usuarios.serializers.usuario_serializers import UsuarioSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UsuarioListCreateView(APIView):
    """
    GET: Lista todos los usuarios con paginación y filtros
    POST: Crea un nuevo usuario
    """
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Lista todos los usuarios con paginación y filtros",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('nombre', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('username', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('cedula', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('theme', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description="Filtra por theme_id"),
        ],
        responses={200: UsuarioSerializer(many=True)}
    )
    def get(self, request):
        # Intentar obtener de cache
        usuarios_list = cache.get("usuarios_list")
        if usuarios_list is None:
            usuarios_list = list(Usuario.objects.select_related('theme').all())
            cache.set("usuarios_list", usuarios_list, timeout=60*5)

        # Convertir lista cacheada a queryset para poder filtrar
        usuarios_qs = Usuario.objects.filter(
            uuid__in=[u.uuid for u in usuarios_list])

        # Filtros básicos de Usuario
        for field in ['nombre', 'username', 'cedula']:
            value = request.GET.get(field)
            if value:
                usuarios_qs = usuarios_qs.filter(
                    **{f"{field}__icontains": value})

        # Filtro directo por theme_id
        theme_id = request.GET.get('theme')
        if theme_id:
            usuarios_qs = usuarios_qs.filter(theme_id=theme_id)

        # Filtros dinámicos de Theme (excepto palette)
        theme_fields = [
            f.name for f in Usuario._meta.get_field('theme').related_model._meta.get_fields()
            if f.concrete and f.name != 'palette'
        ]
        for field in theme_fields:
            value = request.GET.get(f"theme__{field}")
            if value:
                usuarios_qs = usuarios_qs.filter(
                    **{f"theme__{field}__icontains": value})

        # Paginación
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(usuarios_qs, request)
        serializer = UsuarioSerializer(page, many=True)

        total_count = usuarios_qs.count()
        total_pages = (total_count // paginator.get_page_size(request)) + \
                      (1 if total_count % paginator.get_page_size(request) else 0)

        meta = {
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "count": total_count,
            "total_pages": total_pages
        }

        response_data = {
            "status": 200,
            "message": "Elementos paginados correctamente",
            "data": {
                "meta": meta,
                "items": serializer.data
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Crea un nuevo usuario",
        request_body=UsuarioSerializer,
        responses={201: UsuarioSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        usuario = UsuarioService.crear_usuario(request.data)
        cache.delete("usuarios_list")
        return Response(usuario, status=status.HTTP_201_CREATED)


class UsuarioDetailView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Obtener usuario por UUID",
        responses={200: UsuarioSerializer, 404: "Not Found"}
    )
    def get(self, request, uuid):
        usuario = UsuarioService.obtener_usuario(uuid)
        if not usuario:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(usuario, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Actualizar usuario por UUID",
        request_body=UsuarioSerializer,
        responses={200: UsuarioSerializer,
                   400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, uuid):
        usuario = UsuarioService.actualizar_usuario(uuid, request.data)
        if not usuario:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        cache.delete("usuarios_list")
        return Response(usuario, status=status.HTTP_200_OK)
