from usuarios.models.usuario_models import Usuario
from django.contrib.auth.hashers import make_password


class UsuarioRepository:

    @staticmethod
    def crear_usuario(nombre: str, cedula: str, username: str, password: str) -> Usuario:
        """
        Crea un nuevo usuario con password hasheado.
        """
        usuario = Usuario(
            nombre=nombre,
            cedula=cedula,
            username=username,
            password=make_password(password)
        )
        usuario.save()
        return usuario

    @staticmethod
    def obtener_por_uuid(uuid):
        """
        Obtiene un usuario por su UUID.
        """
        try:
            return Usuario.objects.get(uuid=uuid)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def obtener_por_username(username):
        """
        Obtiene un usuario por su username.
        """
        try:
            return Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def listar_todos():
        """
        Devuelve todos los usuarios.
        """
        return Usuario.objects.all()

    @staticmethod
    def actualizar_usuario(usuario: Usuario, **kwargs):
        """
        Actualiza los campos del usuario. Si viene password, lo hashea.
        """
        password = kwargs.pop('password', None)
        for key, value in kwargs.items():
            setattr(usuario, key, value)
        if password:
            usuario.password = make_password(password)
        usuario.save()
        return usuario

    @staticmethod
    def eliminar_usuario(usuario: Usuario):
        """
        Elimina un usuario de la base de datos.
        """
        usuario.delete()
