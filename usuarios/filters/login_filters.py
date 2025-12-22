from usuarios.models.login_models import Login
from django.db.models import Q


class LoginFilter:

    @staticmethod
    def filtrar_por_id(id: int):
        """
        Filtra logins por ID exacto. Devuelve None si no existe.
        """
        return Login.objects.filter(id=id).first()

    @staticmethod
    def filtrar_por_username(username: str):
        """
        Filtra logins por username exacto. Devuelve None si no existe.
        """
        return Login.objects.filter(username=username).first()
