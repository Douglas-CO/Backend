from rest_framework import serializers
from usuarios.models.usuario_models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador principal para el modelo Usuario.
    """
    class Meta:
        model = Usuario
        # Puedes poner '__all__' para todos los campos
        # o listar los que quieras exponer
        fields = ['uuid', 'nombre', 'cedula', 'username',
                  'password', 'created_at', 'modified_at']
        extra_kwargs = {
            # No mostrar la contraseña en las respuestas
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Hashea la contraseña al crear el usuario.
        """
        from django.contrib.auth.hashers import make_password
        validated_data['password'] = make_password(validated_data['password'])
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
