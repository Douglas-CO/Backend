from rest_framework import serializers
from django.db import transaction
from inventario.models.ingreso_material_models import IngresoMaterial, IngresoMaterialDetalle
from inventario.models.producto_models import Producto


class IngresoMaterialProductoSerializer(serializers.Serializer):
    producto = serializers.IntegerField(required=True)
    stock = serializers.IntegerField(required=True, min_value=1)


class IngresoMaterialSerializer(serializers.ModelSerializer):
    productos = IngresoMaterialProductoSerializer(
        many=True,
        required=True
    )

    class Meta:
        model = IngresoMaterial
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

        with transaction.atomic():  # Todo dentro de transacción segura
            # 1️⃣ Crear ingreso material
            ingreso = IngresoMaterial.objects.create(**validated_data)

            # 2️⃣ Recorrer el array y crear detalle + actualizar stock
            for item in productos_data:
                try:
                    producto = Producto.objects.get(id=item['producto'])
                except Producto.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Producto con id {item['producto']} no existe"
                    )

                # Crear detalle del ingreso
                IngresoMaterialDetalle.objects.create(
                    ingreso=ingreso,
                    producto=producto,
                    cantidad=item['stock']
                )

                # Sumar stock al producto
                producto.stock += item['stock']
                producto.save()

        return ingreso
