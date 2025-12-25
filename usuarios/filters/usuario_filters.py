from usuarios.models.usuario_models import Usuario
from django.db.models import Q


class UsuarioFilter:

    @staticmethod
    def filtrar_por_campos(usuario_filters: dict = None, theme_filters: dict = None):
        """
        Filtra usuarios según campos del usuario y del theme.
        - usuario_filters: dict con filtros directos del modelo Usuario
        - theme_filters: dict con filtros para el modelo Theme (ForeignKey), excluye 'palette'
        """
        qs = Usuario.objects.all()

        # Filtros directos de Usuario
        if usuario_filters:
            qs = qs.filter(**usuario_filters)

        # Filtros dinámicos de Theme (excluyendo palette)
        if theme_filters:
            theme_lookups = {}
            for k, v in theme_filters.items():
                if v is not None and k != "palette":  # ignorar palette
                    theme_lookups[f"theme__{k}__icontains"] = v
            if theme_lookups:
                qs = qs.filter(**theme_lookups)

        return qs

    @staticmethod
    def busqueda_general(query: str):
        """
        Búsqueda general en Usuario y Theme de forma dinámica (sin palette)
        """
        return Usuario.objects.filter(
            Q(nombre__icontains=query) |
            Q(username__icontains=query) |
            Q(cedula__icontains=query) |
            Q(theme__name__icontains=query) |
            Q(theme__code__icontains=query) |
            Q(theme__description__icontains=query) |
            Q(theme__state__icontains=query)
        )
