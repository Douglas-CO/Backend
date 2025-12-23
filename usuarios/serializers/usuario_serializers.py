from rest_framework import serializers
from usuarios.models.usuario_models import Usuario
from usuarios.models.theme_models import Theme
from usuarios.serializers.theme_serializers import ThemeSerializer


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador principal para el modelo Usuario, incluyendo datos del theme.
    """
    theme_data = serializers.SerializerMethodField(
        read_only=True)  # nuevo campo

    class Meta:
        model = Usuario
        fields = [
            'uuid', 'nombre', 'cedula', 'username', 'password',
            'created_at', 'modified_at', 'theme', 'theme_data'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_theme_data(self, obj):
        """
        Devuelve los datos completos del theme relacionado
        usando ThemeSerializer, si existe.
        """
        if obj.theme:
            return ThemeSerializer(obj.theme).data
        return None

    def create(self, validated_data):
        """
        Hashea la contraseña al crear el usuario.
        """
        from django.contrib.auth.hashers import make_password
        validated_data['password'] = make_password(validated_data['password'])

        # Si no viene theme, asignar por defecto id=1 si existe
        from usuarios.models.theme_models import Theme
        if 'theme' not in validated_data:
            try:
                validated_data['theme'] = Theme.objects.get(id=1)
            except Theme.DoesNotExist:
                pass  # no hacemos nada, queda vacío

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Hashea la contraseña si se actualiza.
        """
        from django.contrib.auth.hashers import make_password
        password = validated_data.get('password', None)
        if password:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)
