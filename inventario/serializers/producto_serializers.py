from rest_framework import serializers
from inventario.models.producto_models import Producto
from inventario.models.categoria_models import Categoria
from inventario.serializers.categoria_serializers import CategoriaSerializer


class ProductoSerializer(serializers.ModelSerializer):
    categoria_data = serializers.SerializerMethodField(read_only=True)

    # Campo obligatorio y validado
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        required=True,
        error_messages={
            "required": "Requiere seleccionar una categoría",
            "null": "La categoría no puede ser nula",
            "does_not_exist": "La categoría seleccionada no existe",
        }
    )

    class Meta:
        model = Producto
        fields = [
            'uuid', 'name', 'code', 'description', 'state',
            'iva', 'stock', 'valor', 'categoria', 'categoria_data'
        ]

    def get_categoria_data(self, obj):
        return CategoriaSerializer(obj.categoria).data if obj.categoria else None

    def validate(self, attrs):
        """
        - POST: categoría obligatoria
        - PUT: categoría obligatoria
        - PATCH: opcional (si no viene, se conserva)
        """
        # Crear (POST)
        if self.instance is None:
            if not attrs.get('categoria'):
                raise serializers.ValidationError({
                    "categoria": "Requiere seleccionar una categoría"
                })

        # Actualizar (PUT / PATCH)
        else:
            if 'categoria' in attrs and not attrs.get('categoria'):
                raise serializers.ValidationError({
                    "categoria": "La categoría no puede ser nula"
                })

        return attrs
