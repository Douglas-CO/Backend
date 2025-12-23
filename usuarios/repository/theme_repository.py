from django.core.cache import cache
from usuarios.models.theme_models import Theme


class ThemeRepository:

    @staticmethod
    def crear_theme(name: str, code: str, description: str, state: str, palette: str) -> Theme:
        """
        Crea un nuevo theme con password hasheado.
        """
        theme = Theme(
            name=name,
            code=code,
            description=description,
            state=state,
            palette=palette,
        )
        theme.save()
        # Limpiar cache automáticamente
        cache.delete("themes_list")  # Solo borra la lista de themes
        return theme

    @staticmethod
    def obtener_por_uuid(uuid):
        """
        Obtiene un theme por su UUID.
        """
        try:
            return Theme.objects.get(uuid=uuid)
        except Theme.DoesNotExist:
            return None

    @staticmethod
    def obtener_por_name(name):
        """
        Obtiene un theme por su name.
        """
        try:
            return Theme.objects.get(name=name)
        except Theme.DoesNotExist:
            return None

    @staticmethod
    def listar_todos():
        """
        Devuelve todos los themes. Usa cache si está disponible.
        """
        themes = cache.get("themes_list")
        if themes is None:
            themes = list(Theme.objects.all())
            # Cache por 5 minutos
            cache.set("themes_list", themes, timeout=60*5)
        return themes

    @staticmethod
    def actualizar_theme(theme: Theme, **kwargs):
        """
        Actualiza los campos del theme.
        """
        for key, value in kwargs.items():
            setattr(theme, key, value)
        theme.save()
        # Limpiar cache automáticamente
        cache.delete("themes_list")
        return theme
