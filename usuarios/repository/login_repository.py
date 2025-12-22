from usuarios.models.usuario_models import Usuario


class LoginRepository:

    @staticmethod
    def obtener_usuario_por_username(username: str):
        try:
            return Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

    @staticmethod
    def eliminar_token_anterior(usuario_id: int):
        # Borrar login anterior
        login_existente = Login.objects.filter(usuario_id=usuario_id).first()
        if login_existente:
            login_existente.delete()
        # Limpiar cache
        cache.delete(f"usuario_token_{usuario_id}")
