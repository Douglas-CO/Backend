from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usuarios.services.login_services import LoginService
from usuarios.serializers.login_serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from usuarios.services.logout_services import LogoutService
from drf_yasg import openapi
from config.permissions.token_required import TokenRequiredPermission


class LoginView(APIView):
    """
    Endpoint para login de usuario.
    """
    permission_classes = []

    @swagger_auto_schema(
        operation_description="Login de usuario y obtención de token",
        request_body=LoginSerializer,
        responses={200: "Login exitoso", 400: "Credenciales inválidas"}
    )
    def post(self, request):
        try:
            data = LoginService.loggear(request.data)
            return Response({
                "status": 200,
                "message": "Login exitoso",
                "data": data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": 400,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Endpoint para cerrar sesión de un usuario.
    """
    permission_classes = [TokenRequiredPermission]  # Requiere token válido

    @swagger_auto_schema(
        operation_description="Cerrar sesión de un usuario eliminando su token",
        manual_parameters=[
            openapi.Parameter(
                'usuario_id',
                openapi.IN_QUERY,
                description="ID del usuario",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: "Logout exitoso",
            400: "No existe sesión activa para este usuario",
            401: "Token inválido o sesión cerrada"
        }
    )
    def post(self, request):
        usuario_id = request.query_params.get("usuario_id")
        if not usuario_id:
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Se requiere el id del usuario",
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = LogoutService.logout(int(usuario_id))
            return Response({
                "status_code": status.HTTP_200_OK,
                "message": result["message"],
                "data": None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
                "data": None
            }, status=status.HTTP_400_BAD_REQUEST)
