from usuarios.models.theme_models import Theme
from usuarios.repository.usuario_repository import UsuarioRepository
from usuarios.serializers.usuario_serializers import UsuarioSerializer


class UsuarioService:
    """
    Servicio simple para operaciones de negocio sobre Usuario.
    """

    @staticmethod
    def crear_usuario(data: dict):
        payload = data.copy()

        # Default theme si no viene
        if 'theme' not in payload:
            theme = Theme.objects.filter(id=1).first()
            if theme:
                payload['theme'] = theme.id

        serializer = UsuarioSerializer(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def listar_usuarios():
        usuarios = UsuarioRepository.listar_todos()
        return UsuarioSerializer(usuarios, many=True).data

    @staticmethod
    def obtener_usuario(uuid):
        usuario = UsuarioRepository.obtener_por_uuid(uuid)
        if not usuario:
            return None
        return UsuarioSerializer(usuario).data

    @staticmethod
    def actualizar_usuario(uuid, data: dict):
        usuario = UsuarioRepository.obtener_por_uuid(uuid)
        if not usuario:
            return None

        serializer = UsuarioSerializer(
            usuario,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
