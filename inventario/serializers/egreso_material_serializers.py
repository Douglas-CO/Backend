from rest_framework import serializers
from django.db import transaction
from inventario.models.egreso_material_models import EgresoMaterial, EgresoMaterialDetalle
from inventario.models.producto_models import Producto


class EgresoMaterialProductoSerializer(serializers.Serializer):
    producto = serializers.IntegerField(required=True)
    stock = serializers.IntegerField(required=True, min_value=1)


class EgresoMaterialSerializer(serializers.ModelSerializer):
    productos = EgresoMaterialProductoSerializer(
        many=True,
        required=True
    )

    class Meta:
        model = EgresoMaterial
        fields = [
            'uuid',
            'name',
            'type',
            'description',
            'productos',
            'state',
            'created_at',
            'modified_at',
        ]

    def validate_productos(self, value):
        if not value:
            raise serializers.ValidationError(
                "El campo productos no puede estar vacío"
            )
        return value

    def create(self, validated_data):
        productos_data = validated_data.pop('productos')  # Extraemos el array

        with transaction.atomic():
            # Crear el egreso
            egreso = EgresoMaterial.objects.create(**validated_data)

            for item in productos_data:
                try:
                    producto = Producto.objects.get(id=item['producto'])
                except Producto.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Producto con id {item['producto']} no existe"
                    )

                # Validar stock disponible
                if producto.stock < item['stock']:
                    raise serializers.ValidationError(
                        f"No hay suficiente stock para el producto {producto.name} (actual: {producto.stock})"
                    )

                # Crear detalle del egreso
                EgresoMaterialDetalle.objects.create(
                    egreso=egreso,
                    producto=producto,
                    cantidad=item['stock']
                )

                # Restar stock
                producto.stock -= item['stock']
                producto.save()

        return egreso
