from usuarios.models.usuario_models import Usuario
from usuarios.models.theme_models import Theme
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
        Si no se envía 'theme', asigna Theme con id=1 por defecto (si existe).
        """
        if 'theme' not in data:
            try:
                data['theme'] = Theme.objects.get(id=1).id
            except Theme.DoesNotExist:
                pass  # Si no existe el theme 1, no se asigna nada

        serializer = UsuarioSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        return serializer.data  # Devuelve datos serializados, incluyendo theme_data

    @staticmethod
    def listar_usuarios():
        """
        Lista todos los usuarios.
        """
        usuarios = UsuarioRepository.listar_todos()
        # theme_data incluido
        return UsuarioSerializer(usuarios, many=True).data

    @staticmethod
    def obtener_usuario(uuid):
        """
        Obtiene un usuario por UUID.
        """
        usuario = UsuarioRepository.obtener_por_uuid(uuid)
        if not usuario:
            return None
        return UsuarioSerializer(usuario).data  # theme_data incluido

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
        return serializer.data  # theme_data incluido
