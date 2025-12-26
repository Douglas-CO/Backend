from django.urls import path
from venta.views.solicitud_servicio_views import SolicitudServicioListCreateView, SolicitudServicioDetailView, SolicitudServicioUpdateStatusView


urlpatterns = [
    path('solicitud-servicio/', SolicitudServicioListCreateView.as_view(),
         name='solicitud_servicio-list'),
    path('solicitud-servicio/<uuid:uuid>/',
         SolicitudServicioDetailView.as_view(), name='solicitud_servicio-detail'),
    path('solicitud-servicio/<uuid:uuid>/status/',
         SolicitudServicioUpdateStatusView.as_view(), name='solicitud-servicio-update-status'),
]
