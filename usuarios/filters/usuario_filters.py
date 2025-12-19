from usuarios.models.usuario_models import Usuario
from django.db.models import Q


class UsuarioFilter:

    @staticmethod
    def filtrar_por_id(id: int):
        """
        Filtra usuarios cuyo id contenga el number dado (case-insensitive).
        """
        return Usuario.objects.filter(id__icontains=id)

    @staticmethod
    def filtrar_por_nombre(nombre: str):
        """
        Filtra usuarios cuyo nombre contenga el string dado (case-insensitive).
        """
        return Usuario.objects.filter(nombre__icontains=nombre)

    @staticmethod
    def filtrar_por_username(username: str):
        """
        Filtra usuarios por username exacto.
        """
        return Usuario.objects.filter(username=username)

    @staticmethod
    def filtrar_por_cedula(cedula: str):
        """
        Filtra usuarios por cédula exacta.
        """
        return Usuario.objects.filter(cedula=cedula)

    @staticmethod
    def busqueda_general(query: str):
        """
        Búsqueda general en nombre, username o cédula.
        """
        return Usuario.objects.filter(
            Q(nombre__icontains=query) |
            Q(username__icontains=query) |
            Q(cedula__icontains=query)
        )

    @staticmethod
    def activos():
        """
        Si tu modelo tiene un campo de estado o activo, puedes filtrarlos aquí.
        """
        return Usuario.objects.filter(is_active=True)  # ejemplo si agregas is_active
