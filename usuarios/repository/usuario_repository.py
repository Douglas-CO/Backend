from django.core.cache import cache
from django.contrib.auth.hashers import make_password

from usuarios.models.usuario_models import Usuario

class UsuarioRepository:

    @staticmethod
    def crear_usuario(nombre: str, cedula: str, username: str, password: str, theme: int) -> Usuario:
        """
        Crea un nuevo usuario con password hasheado.
        """
        usuario = Usuario(
            nombre=nombre,
            cedula=cedula,
            username=username,
            password=make_password(password),
            theme=theme
        )
        usuario.save()
        # Limpiar cache automáticamente
        cache.delete("usuarios_list")  # Solo borra la lista de usuarios
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
    def listar_todos():
        """
        Devuelve todos los usuarios. Usa cache si está disponible.
        """
        usuarios = cache.get("usuarios_list")
        if usuarios is None:
            usuarios = list(Usuario.objects.all())
            # Cache por 5 minutos
            cache.set("usuarios_list", usuarios, timeout=60*5)
        return usuarios

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
        # Limpiar cache automáticamente
        cache.delete("usuarios_list")
        return usuario
