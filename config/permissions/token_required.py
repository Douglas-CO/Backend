# config/permissions/token_required.py
from rest_framework.permissions import BasePermission
from usuarios.models.login_models import Login


class TokenRequiredPermission(BasePermission):
    """
    Verifica que el request tenga un header Authorization con un token válido
    que exista en la tabla usuarios_login.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            self.message = "No se envió ningún token"
            return False

        # Aceptar Token <token> o Bearer <token>
        if auth_header.startswith("Token "):
            token = auth_header.split(" ")[1]
        elif auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            self.message = "Formato de token inválido. Usa 'Token <token>' o 'Bearer <token>'."
            return False

        # Verificar token en la tabla usuarios_login
        login_existente = Login.objects.filter(token=token).first()
        if not login_existente:
            self.message = "Token inválido o sesión cerrada."
            return False

        # Agregar usuario al request (opcional)
        request.usuario = login_existente.usuario
        return True
