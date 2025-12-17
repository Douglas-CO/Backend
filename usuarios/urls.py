from django.urls import path
from usuarios.views.usuario_views import UsuarioListCreateView, UsuarioDetailView

urlpatterns = [
    path('', UsuarioListCreateView.as_view(), name='usuarios-list'),
    path('<uuid:uuid>/', UsuarioDetailView.as_view(), name='usuarios-detail'),
]
