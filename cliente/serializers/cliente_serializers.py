from rest_framework import serializers
from cliente.models.cliente_models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'uuid',
            'identificacion',
            'nombre',
            'direccion',
            'fecha_nacimiento',
            'sexo',
            'is_discapacitado',
            'is_tercera_edad',
            'state',
            'created_at',
            'modified_at',
        ]
    
    def get_sexo(self, obj):
        # Mapea cualquier valor a lo que quieres mostrar
        if obj.sexo in ("H", "HOMBRE"):
            return "HOMBRE"
        if obj.sexo in ("M", "MUJER"):
            return "MUJER"
        return obj.sexo