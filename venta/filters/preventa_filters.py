from venta.models.preventa_models import Preventa

class PreventaFilter:

    @staticmethod
    def base_queryset():
        return Preventa.objects.select_related(
            "solicitud_servicio",
            "solicitud_servicio__usuario"
        )

    @staticmethod
    def apply_filters(params: dict):
        qs = PreventaFilter.base_queryset()

        # -------- Preventa --------
        if params.get("preventa_status"):
            qs = qs.filter(status=params["preventa_status"])

        if params.get("usuario"):
            qs = qs.filter(usuario_id=params["usuario"])

        # -------- SolicitudServicio --------
        if params.get("nombre"):
            qs = qs.filter(
                solicitud_servicio__nombre__icontains=params["nombre"]
            )

        if params.get("identificacion"):
            qs = qs.filter(
                solicitud_servicio__identificacion=params["identificacion"]
            )

        if params.get("email"):
            qs = qs.filter(
                solicitud_servicio__email__icontains=params["email"]
            )

        if params.get("celular"):
            qs = qs.filter(
                solicitud_servicio__celular=params["celular"]
            )

        if params.get("sexo"):
            qs = qs.filter(
                solicitud_servicio__sexo=params["sexo"]
            )

        if params.get("solicitud_status"):
            qs = qs.filter(
                solicitud_servicio__status=params["solicitud_status"]
            )

        if params.get("coord"):
            qs = qs.filter(
                solicitud_servicio__coord__icontains=params["coord"]
            )

        if params.get("is_discapacitado") is not None:
            qs = qs.filter(
                solicitud_servicio__is_discapacitado=params["is_discapacitado"]
            )

        if params.get("is_tercera_edad") is not None:
            qs = qs.filter(
                solicitud_servicio__is_tercera_edad=params["is_tercera_edad"]
            )

        # -------- Usuario --------
        if params.get("usuario_nombre"):
            qs = qs.filter(
                solicitud_servicio__usuario__nombre__icontains=params["usuario_nombre"]
            )

        if params.get("usuario_username"):
            qs = qs.filter(
                solicitud_servicio__usuario__username__icontains=params["usuario_username"]
            )

        if params.get("usuario_cedula"):
            qs = qs.filter(
                solicitud_servicio__usuario__cedula=params["usuario_cedula"]
            )

        return qs
