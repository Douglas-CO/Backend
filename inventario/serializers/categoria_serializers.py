from rest_framework import serializers
from inventario.models.categoria_models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['uuid', 'name', 'code', 'description',
                  'state', 'created_at', 'modified_at']