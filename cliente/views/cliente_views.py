from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache

from config.permissions.token_required import TokenRequiredPermission
from config.views.pagination import StandardResultsSetPagination

from cliente.models.cliente_models import Cliente
from cliente.services.cliente_services import ClienteService
from cliente.serializers.cliente_serializers import ClienteSerializer


class ClienteListCreateView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Lista clientes con paginación y filtros",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('nombre', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('identificacion', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('state', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
        responses={200: ClienteSerializer(many=True)}
    )
    def get(self, request):
        clientes_list = cache.get("clientes_list")
        if clientes_list is None:
            clientes_list = Cliente.objects.all()
            cache.set("clientes_list", clientes_list, timeout=60 * 5)

        clientes_qs = clientes_list

        # 🔍 Filtros
        nombre = request.GET.get("nombre")
        identificacion = request.GET.get("identificacion")
        state = request.GET.get("state")

        if nombre:
            clientes_qs = clientes_qs.filter(nombre__icontains=nombre)

        if identificacion:
            clientes_qs = clientes_qs.filter(identificacion__icontains=identificacion)

        if state:
            if state.lower() in ("true", "1"):
                clientes_qs = clientes_qs.filter(state=True)
            elif state.lower() in ("false", "0"):
                clientes_qs = clientes_qs.filter(state=False)

        # 📄 Paginación
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(clientes_qs, request)
        serializer = ClienteSerializer(page, many=True)

        total_count = clientes_qs.count()
        page_size = paginator.get_page_size(request)
        total_pages = (total_count // page_size) + (1 if total_count % page_size else 0)

        return Response(
            {
                "status": 200,
                "message": "Clientes paginados correctamente",
                "data": {
                    "meta": {
                        "next": paginator.get_next_link(),
                        "previous": paginator.get_previous_link(),
                        "count": total_count,
                        "total_pages": total_pages
                    },
                    "items": serializer.data
                }
            },
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Crear cliente",
        request_body=ClienteSerializer,
        responses={201: ClienteSerializer}
    )
    def post(self, request):
        cliente = ClienteService.create_cliente(request.data)
        cache.delete("clientes_list")

        return Response(
            {
                "status": 201,
                "message": "Cliente creado correctamente",
                "data": cliente
            },
            status=status.HTTP_201_CREATED
        )


class ClienteDetailView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Obtener cliente por UUID",
        responses={200: ClienteSerializer, 404: "Not Found"}
    )
    def get(self, request, uuid):
        cliente = ClienteService.get_uuid(uuid)
        if not cliente:
            return Response(
                {"status": 404, "message": "Cliente no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"status": 200, "message": "OK", "data": cliente},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        operation_description="Actualizar cliente por UUID",
        request_body=ClienteSerializer,
        responses={200: ClienteSerializer, 404: "Not Found"}
    )
    def patch(self, request, uuid):
        cliente = ClienteService.upd_cliente(uuid, request.data)
        if not cliente:
            return Response(
                {"status": 404, "message": "Cliente no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        cache.delete("clientes_list")

        return Response(
            {
                "status": 200,
                "message": "Cliente actualizado correctamente",
                "data": cliente
            },
            status=status.HTTP_200_OK
        )


class ClienteByCedulaView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Buscar cliente por cédula (BD → Registro Civil)",
        responses={200: ClienteSerializer, 404: "Not Found"}
    )
    def get(self, request, cedula):
        result = ClienteService.get_by_cedula(cedula)
        if not result:
            return Response(
                {"status": 404, "message": "Cédula no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "status": 200,
                "message": "OK",
                **result
            },
            status=status.HTTP_200_OK
        )
