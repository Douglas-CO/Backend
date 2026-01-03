from rest_framework import serializers
from django.db import transaction

from venta.models.preventa_models import Preventa, PreventaDetalle
from inventario.models.producto_models import Producto


class PreventaProductoSerializer(serializers.Serializer):
    producto = serializers.IntegerField(required=True)
    cantidad = serializers.IntegerField(min_value=1, required=True)


class PreventaSerializer(serializers.ModelSerializer):
    productos = PreventaProductoSerializer(many=True, write_only=True)

    class Meta:
        model = Preventa
        fields = [
            'uuid',
            'solicitud_servicio',
            'usuario',
            'status',
            'productos',
            'created_at',
            'modified_at',
        ]
        read_only_fields = ('uuid', 'created_at', 'modified_at')

    def validate_productos(self, value):
        if not value:
            raise serializers.ValidationError("El campo productos no puede estar vacío")

        productos_ids = [p["producto"] for p in value]

        existentes = set(
            Producto.objects.filter(id__in=productos_ids)
            .values_list("id", flat=True)
        )

        invalidos = set(productos_ids) - existentes
        if invalidos:
            raise serializers.ValidationError(
                f"Productos no existen: {list(invalidos)}"
            )

        return value

    @transaction.atomic
    def create(self, validated_data):
        productos = validated_data.pop("productos")

        preventa = Preventa.objects.create(**validated_data)

        PreventaDetalle.objects.bulk_create([
            PreventaDetalle(
                preventa=preventa,
                producto_id=item["producto"],
                cantidad=item["cantidad"]
            )
            for item in productos
        ])

        return preventa
