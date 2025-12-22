from usuarios.models.login_models import Login
from django.core.cache import cache


class LogoutService:

    @staticmethod
    def logout(usuario_id: int):
        login = Login.objects.filter(usuario_id=usuario_id).first()
        if not login:
            raise Exception("No existe sesión activa para este usuario")

        # Eliminar de la DB
        login.delete()

        # Limpiar cache
        cache.delete(f"usuario_token_{usuario_id}")

        return {"message": "Logout exitoso"}
