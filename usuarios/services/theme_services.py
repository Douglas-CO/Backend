from usuarios.models.theme_models import Theme
from usuarios.repository.theme_repository import ThemeRepository
from usuarios.serializers.theme_serializers import ThemeSerializer


class ThemeService:

    @staticmethod
    def crear_theme(data: dict):
        serializer = ThemeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        theme = serializer.save()
        return serializer.data

    @staticmethod
    def listar_theme():
        themes = ThemeRepository.listar_todos()
        return ThemeSerializer(themes, many=True).data

    @staticmethod
    def obtener_theme(uuid):
        theme = ThemeRepository.obtener_por_uuid(uuid)
        if not theme:
            return None
        return ThemeSerializer(theme).data

    @staticmethod
    def actualizar_theme(uuid, data: dict):
        theme = ThemeRepository.obtener_por_uuid(uuid)
        if not theme:
            return None
        serializer = ThemeSerializer(theme, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        theme = serializer.save()
        return serializer.data
