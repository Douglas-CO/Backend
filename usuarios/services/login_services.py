from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from usuarios.repository.login_repository import LoginRepository
from usuarios.serializers.login_serializers import LoginSerializer
from usuarios.models.login_models import Login


class LoginService:

    @staticmethod
    def loggear(data: dict):
        # 1. Validar datos de login
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        force = serializer.validated_data.get('force', False)

        # 2. Obtener usuario
        usuario = LoginRepository.obtener_usuario_por_username(username)
        if not usuario:
            raise Exception("Usuario no existe")

        # 3. Verificar contraseña
        if not check_password(password, usuario.password):
            raise Exception("Contraseña incorrecta")

        # 4. Verificar sesión existente
        sesion_existente = Login.objects.filter(usuario_id=usuario.id).first()
        if sesion_existente:
            if not force:
                raise Exception(
                    "Sesión ya se encuentra abierta en otro dispositivo")
            else:
                # Eliminar sesión anterior
                sesion_existente.delete()
                cache.delete(f"usuario_token_{usuario.id}")

        # 5. Generar nuevo token
        refresh = RefreshToken.for_user(usuario)
        access_token = str(refresh)

        # 6. Guardar nuevo login en la tabla
        login_obj = Login.objects.create(
            usuario_id=usuario.id,
            token=access_token,
            force=force,
        )

        # 7. Guardar token en cache individual
        cache.set(f"usuario_token_{usuario.id}", access_token, timeout=3600)

        # 8. Actualizar cache de lista de logins (opcional)
        cache.delete("login_list")
        logins = list(Login.objects.all())
        cache.set("login_list", logins, timeout=300)

        # 9. Retornar datos
        return {
            "usuario": {
                "id": usuario.id,
                "uuid": usuario.uuid,
                "nombre": usuario.nombre,
                "username": usuario.username
            },
            "access_token": access_token,
            "refresh_token": str(refresh)
        }
