from django.urls import path
from inventario.views.categoria_views import CategoriaListCreateView, CategoriaDetailView
from inventario.views.producto_views import ProductoListCreateView, ProductoDetailView

urlpatterns = [
    path('categoria/', CategoriaListCreateView.as_view(), name='categoria-list'),
    path('categoria/<uuid:uuid>/',
         CategoriaDetailView.as_view(), name='categoria-detail'),

    path('producto/', ProductoListCreateView.as_view(), name='producto-list'),
    path('producto/<uuid:uuid>/',
         ProductoDetailView.as_view(), name='producto-detail'),
]
