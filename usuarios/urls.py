from django.urls import path
from usuarios.views.usuario_views import UsuarioListCreateView, UsuarioDetailView
from usuarios.views.login_views import LoginView, LogoutView
from usuarios.views.theme_views import ThemeListCreateView, ThemeDetailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/out/', LogoutView.as_view(), name='logout'),
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuarios-list'),
    path('usuarios/<uuid:uuid>/',
         UsuarioDetailView.as_view(), name='usuarios-detail'),
    path('theme/', ThemeListCreateView.as_view(), name='theme-list'),
    path('theme/<uuid:uuid>/', ThemeDetailView.as_view(), name='theme-detail'),
]
