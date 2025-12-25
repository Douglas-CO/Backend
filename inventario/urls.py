from django.urls import path
from inventario.views.categoria_views import CategoriaListCreateView, CategoriaDetailView

urlpatterns = [
    path('categoria/', CategoriaListCreateView.as_view(), name='categoria-list'),
    path('categoria/<uuid:uuid>/',
         CategoriaDetailView.as_view(), name='categoria-detail'),
]
