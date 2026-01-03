from rest_framework import status as drf_status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from config.views.pagination import StandardResultsSetPagination
from config.permissions.token_required import TokenRequiredPermission
from config.choices.venta_choices import STATUS_CHOICES

from venta.services.preventa_services import PreventaService
from venta.filters.preventa_filters import PreventaFilter
from venta.serializers.preventa_serializers import PreventaSerializer
from venta.models.preventa_models import Preventa


class PreventaListCreateView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Lista preventas con filtros y paginación",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY,
                              type=openapi.TYPE_INTEGER),

            # -------- Preventa --------
            openapi.Parameter('status',
                              openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('usuario',
                              openapi.IN_QUERY, type=openapi.TYPE_INTEGER,description="ID del usuario creador"),

            # -------- SolicitudServicio --------
            openapi.Parameter('nombre', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('identificacion', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('celular', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('sexo', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('solicitud_status',
                              openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('coord', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('is_discapacitado',
                              openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('is_tercera_edad',
                              openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),

            # -------- Usuario --------
            openapi.Parameter('usuario_nombre', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
            openapi.Parameter('usuario_username',
                              openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('usuario_cedula', openapi.IN_QUERY,
                              type=openapi.TYPE_STRING),
        ],
        responses={200: PreventaSerializer(many=True)}
    )
    def get(self, request):
        params = request.query_params.dict()

        queryset = PreventaFilter.apply_filters(params)

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)

        serializer = PreventaSerializer(page, many=True)

        return paginator.get_paginated_response({
            "items": serializer.data
        })

    @swagger_auto_schema(
        operation_description="Crear una nueva preventa",
        request_body=PreventaSerializer,
        responses={201: PreventaSerializer}
    )
    def post(self, request):
        preventa = PreventaService.create_preventa(request.data)
        return Response(preventa, status=drf_status.HTTP_201_CREATED)


class PreventaDetailView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Obtener preventa por UUID",
        responses={200: PreventaSerializer, 404: "Not Found"}
    )
    def get(self, request, uuid):
        preventa = PreventaService.get_preventa(uuid)
        if not preventa:
            return Response(
                {"detail": "Preventa no encontrada"},
                status=drf_status.HTTP_404_NOT_FOUND
            )
        return Response(preventa, status=drf_status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Actualizar preventa (parcial)",
        request_body=PreventaSerializer,
        responses={200: PreventaSerializer}
    )
    def patch(self, request, uuid):
        preventa = PreventaService.upd_preventa(uuid, request.data)
        if not preventa:
            return Response(
                {"detail": "Preventa no encontrada"},
                status=drf_status.HTTP_404_NOT_FOUND
            )
        return Response(preventa, status=drf_status.HTTP_200_OK)


class PreventaUpdateStatusView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Actualizar estado de una preventa",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["status"],
            properties={
                "status": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Nuevo estado de la preventa"
                )
            }
        ),
        responses={200: PreventaSerializer,
                   400: "Bad Request", 404: "Not Found"}
    )
    def patch(self, request, uuid):
        status_value = request.data.get("status")
        allowed_status = [choice[0] for choice in STATUS_CHOICES]

        if status_value not in allowed_status:
            return Response(
                {"detail": f"Status inválido. Debe ser uno de {allowed_status}"},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        try:
            preventa = Preventa.objects.get(uuid=uuid)
        except Preventa.DoesNotExist:
            return Response(
                {"detail": "Preventa no encontrada"},
                status=drf_status.HTTP_404_NOT_FOUND
            )

        preventa.status = status_value
        preventa.save()

        serializer = PreventaSerializer(preventa)
        return Response(serializer.data, status=drf_status.HTTP_200_OK)
