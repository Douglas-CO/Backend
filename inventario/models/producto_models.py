import uuid
from django.db import models
from config.models.AuditDateModel import AuditDateModel
from inventario.models.categoria_models import Categoria


class Producto(AuditDateModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, editable=False, unique=True)
    description = models.CharField(max_length=255)
    state = models.BooleanField(default=True)

    iva = models.IntegerField()
    stock = models.IntegerField()
    valor = models.DecimalField(
        max_digits=100,  
        decimal_places=2
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="productos"
    )

    def __str__(self):
        return self.name
