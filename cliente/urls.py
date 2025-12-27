from django.urls import path
from cliente.views.cliente_views import (
    ClienteListCreateView,
    ClienteDetailView,
    ClienteByCedulaView
)
urlpatterns = [
    path("clientes/", ClienteListCreateView.as_view()),
    path("clientes/<uuid:uuid>/", ClienteDetailView.as_view()),
    path("clientes/cedula/<str:cedula>/", ClienteByCedulaView.as_view()),
]
