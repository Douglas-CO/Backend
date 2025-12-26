from rest_framework import status as drf_status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework import status
from drf_yasg import openapi

from config.views.pagination import StandardResultsSetPagination
from venta.models.solicitud_servicio_models import SolicitudServicio
from config.permissions.token_required import TokenRequiredPermission
from venta.services.solicitud_servicio_services import SolicitudServicioService
from venta.serializers.solicitud_servicio_serializers import SolicitudServicioSerializer


class SolicitudServicioListCreateView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Lista de solicitudes de servicios con filtros y paginación",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('nombre', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('identificacion', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('celular', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('sexo', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('coord', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('is_discapacitado', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('is_tercera_edad', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('usuario', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: SolicitudServicioSerializer(many=True)}
    )
    def get(self, request):
        qs = cache.get("solicitud_servicios_qs")

        if qs is None:
            qs = SolicitudServicio.objects.select_related('usuario').all()
            cache.set("solicitud_servicios_qs", qs, timeout=60)

        # 🔎 Filtros seguros
        filters = {}

        if request.GET.get("nombre"):
            filters["nombre__icontains"] = request.GET["nombre"]

        if request.GET.get("identificacion"):
            filters["identificacion__icontains"] = request.GET["identificacion"]

        if request.GET.get("is_discapacitado") is not None:
            filters["is_discapacitado"] = request.GET.get("is_discapacitado").lower() == "true"

        
        if request.GET.get("is_tercera_edad") is not None:
            filters["is_tercera_edad"] = request.GET.get("is_tercera_edad").lower() == "true"

        if request.GET.get("usuario"):
            filters["usuario_id"] = request.GET["usuario"]

        qs = qs.filter(**filters)

        # 📄 Paginación
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(qs, request)
        serializer = SolicitudServicioSerializer(page, many=True)

        return paginator.get_paginated_response({
            "items": serializer.data
        })

    @swagger_auto_schema(
        operation_description="Crear solicitud_servicio",
        request_body=SolicitudServicioSerializer,
        responses={201: SolicitudServicioSerializer}
    )
    def post(self, request):
        solicitud_servicio = SolicitudServicioService.create_solicitud_servicio(request.data)
        cache.delete("solicitud_servicios_qs")
        return Response(solicitud_servicio, status=status.HTTP_201_CREATED)


class SolicitudServicioDetailView(APIView):
    permission_classes = [TokenRequiredPermission]

    @swagger_auto_schema(
        operation_description="Obtener solicitud_servicio por UUID",
        responses={200: SolicitudServicioSerializer, 404: "Not Found"}
    )
    def get(self, request, uuid):
        solicitud_servicio = SolicitudServicioService.get_solicitud_servicio(uuid)
        if not solicitud_servicio:
            return Response(
                {"detail": "SolicitudServicio no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(solicitud_servicio, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Actualizar solicitud_servicio por UUID",
        request_body=SolicitudServicioSerializer,
        responses={200: SolicitudServicioSerializer}
    )
    def patch(self, request, uuid):
        solicitud_servicio = SolicitudServicioService.upd_solicitud_servicio(uuid, request.data)
        if not solicitud_servicio:
            return Response(
                {"detail": "SolicitudServicio no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        cache.delete("solicitud_servicios_qs")
        return Response(solicitud_servicio, status=status.HTTP_200_OK)

class SolicitudServicioUpdateStatusView(APIView):
    permission_classes = [TokenRequiredPermission]

    def patch(self, request, uuid):
        status_value = request.data.get("status")
        allowed_status = ["PENDIENTE", "FINALIZADO", "FALLIDO"]

        if status_value not in allowed_status:
            return Response(
                {"detail": f"Status inválido. Debe ser uno de {allowed_status}"},
                status=drf_status.HTTP_400_BAD_REQUEST
            )

        try:
            solicitud = SolicitudServicio.objects.get(uuid=uuid)
        except SolicitudServicio.DoesNotExist:
            return Response(
                {"detail": "Solicitud Servicio no encontrado"},
                status=drf_status.HTTP_404_NOT_FOUND
            )

        solicitud.status = status_value
        solicitud.save()

        serializer = SolicitudServicioSerializer(solicitud)
        return Response(serializer.data, status=drf_status.HTTP_200_OK)