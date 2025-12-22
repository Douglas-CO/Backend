from django.urls import path
from usuarios.views.usuario_views import UsuarioListCreateView, UsuarioDetailView
from usuarios.views.login_views import LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/out/', LogoutView.as_view(), name='logout'),
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuarios-list'),
    path('usuarios/<uuid:uuid>/',
         UsuarioDetailView.as_view(), name='usuarios-detail'),
]
