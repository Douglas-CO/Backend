from usuarios.models.usuario_models import Usuario
from usuarios.repository.usuario_repository import UsuarioRepository
from usuarios.serializers.usuario_serializers import UsuarioSerializer


class UsuarioService:
    """
    Servicio simple para operaciones de negocio sobre Usuario.
    """

    @staticmethod
    def crear_usuario(data: dict):
        """
        Crea un usuario usando UsuarioSerializer.
        """
        serializer = UsuarioSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        return serializer.data  # Devuelve datos serializados

    @staticmethod
    def listar_usuarios():
        """
        Lista todos los usuarios.
        """
        usuarios = UsuarioRepository.listar_todos()
        return UsuarioSerializer(usuarios, many=True).data

    @staticmethod
    def obtener_usuario(uuid):
        """
        Obtiene un usuario por UUID.
        """
        usuario = UsuarioRepository.obtener_por_uuid(uuid)
        if not usuario:
            return None
        return UsuarioSerializer(usuario).data

    @staticmethod
    def actualizar_usuario(uuid, data: dict):
        """
        Actualiza un usuario por UUID.
        """
        usuario = UsuarioRepository.obtener_por_uuid(uuid)
        if not usuario:
            return None
        serializer = UsuarioSerializer(usuario, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        return serializer.data
