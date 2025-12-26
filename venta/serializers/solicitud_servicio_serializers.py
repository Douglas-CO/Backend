from rest_framework import serializers

from config.utils.validation import validar_cedula_ecuador
from usuarios.models.usuario_models import Usuario
from venta.models.solicitud_servicio_models import SolicitudServicio
from usuarios.serializers.usuario_serializers import UsuarioSerializer


class SolicitudServicioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        error_messages={"invalid": "Email inválido"})
    usuario_data = serializers.SerializerMethodField(read_only=True)

    # Campo obligatorio y validado
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(),
        required=True,
        error_messages={
            "required": "Requiere seleccionar usuario",
            "null": "El usuario no puede ser nula",
            "does_not_exist": "El usuario seleccionado no existe",
        }
    )

    def validate_identificacion(self, value):
        if not validar_cedula_ecuador(value):
            raise serializers.ValidationError("Cédula inválida")
        return value

    class Meta:
        model = SolicitudServicio
        fields = [
            'uuid', 'nombre', 'identificacion', 'celular', 'email',
            'sexo', 'coord', 'is_discapacitado', 'is_tercera_edad',
            'status', 'usuario', 'usuario_data'
        ]

    def get_usuario_data(self, obj):
        return UsuarioSerializer(obj.usuario).data if obj.usuario else None

    def validate(self, attrs):
        """
        - POST: usuario obligatorio
        - PUT: usuario obligatorio
        - PATCH: opcional (si no viene, se conserva)
        """
        # Crear (POST)
        if self.instance is None:
            if not attrs.get('usuario'):
                raise serializers.ValidationError({
                    "usuario": "Requiere seleccionar una usuario"
                })

        # Actualizar (PUT / PATCH)
        else:
            if 'usuario' in attrs and not attrs.get('usuario'):
                raise serializers.ValidationError({
                    "usuario": "La usuario no puede ser nula"
                })

        return attrs
