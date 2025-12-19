from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

from usuarios.models.usuario_models import Usuario
from usuarios.services.usuario_services import UsuarioService
from usuarios.serializers.usuario_serializers import UsuarioSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # <-- valor por defecto
    page_size_query_param = 'page_size'
    max_page_size = 100


class UsuarioListCreateView(APIView):
    """
    GET: Lista todos los usuarios con paginación y filtros
    POST: Crea un nuevo usuario
    """

    @swagger_auto_schema(
        operation_description="Lista todos los usuarios con paginación y filtros",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY,
                              description="Número de página", type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              description="Cantidad por página", type=openapi.TYPE_INTEGER),
            openapi.Parameter('nombre', openapi.IN_QUERY,
                              description="Filtra por nombre", type=openapi.TYPE_STRING),
            openapi.Parameter('username', openapi.IN_QUERY,
                              description="Filtra por username", type=openapi.TYPE_STRING),
            openapi.Parameter('cedula', openapi.IN_QUERY,
                              description="Filtra por cédula", type=openapi.TYPE_STRING),
        ],
        responses={200: UsuarioSerializer(many=True)}
    )
    def get(self, request):
        # Intentar obtener de cache
        usuarios_list = cache.get("usuarios_list")
        if usuarios_list is None:
            usuarios_list = list(Usuario.objects.all())
            cache.set("usuarios_list", usuarios_list, timeout=60*5)

        # Convertir lista cacheada a queryset para poder filtrar
        usuarios_qs = Usuario.objects.filter(
            uuid__in=[u.uuid for u in usuarios_list])

        # Aplicar filtros
        nombre = request.GET.get('nombre')
        username = request.GET.get('username')
        cedula = request.GET.get('cedula')

        if nombre:
            usuarios_qs = usuarios_qs.filter(nombre__icontains=nombre)
        if username:
            usuarios_qs = usuarios_qs.filter(username=username)
        if cedula:
            usuarios_qs = usuarios_qs.filter(cedula=cedula)

        # Paginación
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(usuarios_qs, request)
        serializer = UsuarioSerializer(page, many=True)

        # Meta información
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
        # Limpiar cache automáticamente al crear un usuario
        cache.delete("usuarios_list")
        return Response(usuario, status=status.HTTP_201_CREATED)


class UsuarioDetailView(APIView):
    """
    GET: Obtener un usuario por UUID
    PATCH: Actualizar un usuario por UUID
    """

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
        return Response(usuario, status=status.HTTP_200_OK)
