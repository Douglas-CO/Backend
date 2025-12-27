from django.core.cache import cache
from typing import Optional

from cliente.repository.cliente_repository import ClienteRepository
from cliente.serializers.cliente_serializers import ClienteSerializer
from config.services.registro_civil_service import RegistroCivilService


class ClienteService:

    @staticmethod
    def create_cliente(data: dict) -> dict:
        serializer = ClienteSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        cliente = ClienteRepository.create_cliente(
            **serializer.validated_data
        )

        return ClienteSerializer(cliente).data

    @staticmethod
    def get_all() -> list:
        clientes = ClienteRepository.get_all()
        return ClienteSerializer(clientes, many=True).data

    @staticmethod
    def get_by_cedula(cedula: str) -> Optional[dict]:
        # 1️⃣ Buscar en BD
        cliente = ClienteRepository.get_by_cedula(cedula)
        if cliente:
            return {
                "source": "database",
                "data": ClienteSerializer(cliente).data
            }

        # 2️⃣ Gateway Registro Civil (SOLO GET)
        persona = RegistroCivilService.get_persona_by_cedula(cedula)
        if not persona:
            return None

        # 3️⃣ Mapear respuesta (NO guardar)
        data = {
            "identificacion": persona.get("NUI"),
            "nombre": persona.get("Nombre"),
            "direccion": persona.get("Domicilio"),
            "fecha_nacimiento": persona.get("FechaNacimiento"),
            "sexo": persona.get("Sexo"),
        }

        return {
            "source": "registro_civil",
            "data": data
        }

    @staticmethod
    def get_uuid(uuid) -> Optional[dict]:
        cliente = ClienteRepository.get_by_uuid(uuid)
        if not cliente:
            return None

        return ClienteSerializer(cliente).data

    @staticmethod
    def upd_cliente(uuid, data: dict) -> Optional[dict]:
        cliente = ClienteRepository.get_by_uuid(uuid)
        if not cliente:
            return None

        serializer = ClienteSerializer(cliente, data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        for field, value in serializer.validated_data.items():
            setattr(cliente, field, value)

        cliente.save()

        cache.delete("clientes:list")
        cache.delete(f"cliente:cedula:{cliente.identificacion}")

        return ClienteSerializer(cliente).data
