from django.urls import path
from inventario.views.categoria_views import CategoriaListCreateView, CategoriaDetailView
from inventario.views.producto_views import ProductoListCreateView, ProductoDetailView
from inventario.views.ingreso_material_views import IngresoMaterialListCreateView, IngresoMaterialDetailView
from inventario.views.egreso_material_views import EgresoMaterialListCreateView, EgresoMaterialDetailView

urlpatterns = [
    path('categoria/', CategoriaListCreateView.as_view(), name='categoria-list'),
    path('categoria/<uuid:uuid>/',
         CategoriaDetailView.as_view(), name='categoria-detail'),

    path('producto/', ProductoListCreateView.as_view(), name='producto-list'),
    path('producto/<uuid:uuid>/',
         ProductoDetailView.as_view(), name='producto-detail'),

    path('ingreso-material/', IngresoMaterialListCreateView.as_view(), name='ingreso-material-list'),
    path('ingreso-material/<uuid:uuid>/',
         IngresoMaterialDetailView.as_view(), name='ingreso-material-detail'),
     path('egreso-material/', EgresoMaterialListCreateView.as_view(), name='egreso-material-list'),
    path('egreso-material/<uuid:uuid>/',
         EgresoMaterialDetailView.as_view(), name='egreso-material-detail'),
]
