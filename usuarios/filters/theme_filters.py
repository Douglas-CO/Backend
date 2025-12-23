from usuarios.models.theme_models import Theme


class ThemeFilter:

    @staticmethod
    def filtrar_por_id(id: int):
        return Theme.objects.filter(id=id)

    @staticmethod
    def filtrar_por_name(name: str):
        return Theme.objects.filter(name__icontains=name)

    @staticmethod
    def filtrar_por_code(code: str):
        return Theme.objects.filter(code=code)

    @staticmethod
    def filtrar_por_description(description: str):
        return Theme.objects.filter(description__icontains=description)

    @staticmethod
    def filtrar_por_state(state: bool):
        return Theme.objects.filter(state=state)
