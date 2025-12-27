from django.core.cache import cache
from typing import Optional

from datetime import date
from cliente.models.cliente_models import Cliente


class ClienteRepository:

    @staticmethod
    def create_cliente(
        identificacion: str,
        nombre: str,
        direccion: str,
        fecha_nacimiento: date,
        sexo: str,
        is_discapacitado: bool = False,
        is_tercera_edad: bool = False,
        state: bool = True,
    ) -> Cliente:

        cliente = Cliente.objects.create(
            identificacion=identificacion,
            nombre=nombre,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            is_discapacitado=is_discapacitado,
            is_tercera_edad=is_tercera_edad,
            state=state,
        )

        # invalidar cache
        cache.delete("clientes:list")
        cache.delete(f"cliente:cedula:{identificacion}")

        return cliente

    @staticmethod
    def get_by_uuid(uuid) -> Optional[Cliente]:
        return Cliente.objects.filter(uuid=uuid).first()

    @staticmethod
    def get_by_cedula(cedula: str) -> Optional[Cliente]:
        cache_key = f"cliente:cedula:{cedula}"

        cliente = cache.get(cache_key)
        if cliente:
            return cliente

        cliente = Cliente.objects.filter(identificacion=cedula).first()
        if cliente:
            cache.set(cache_key, cliente, timeout=60 * 10)

        return cliente

    @staticmethod
    def get_all():
        cache_key = "clientes:list"
        clientes = cache.get(cache_key)

        if clientes is None:
            clientes = list(Cliente.objects.filter(state=True))
            cache.set(cache_key, clientes, timeout=60 * 5)

        return clientes