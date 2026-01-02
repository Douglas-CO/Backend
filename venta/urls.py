from django.urls import path
from venta.views.solicitud_servicio_views import (
    SolicitudServicioListCreateView, SolicitudServicioDetailView, SolicitudServicioUpdateStatusView)
from venta.views.preventa_views import (
    PreventaListCreateView,
    PreventaDetailView,
    PreventaUpdateStatusView
)


urlpatterns = [
    path('solicitud-servicio/', SolicitudServicioListCreateView.as_view(),
         name='solicitud_servicio-list'),
    path('solicitud-servicio/<uuid:uuid>/',
         SolicitudServicioDetailView.as_view(), name='solicitud_servicio-detail'),
    path('solicitud-servicio/<uuid:uuid>/status/',
         SolicitudServicioUpdateStatusView.as_view(), name='solicitud-servicio-update-status'),

    path('preventas/', PreventaListCreateView.as_view(),
         name='preventa-list-create'),
    path('preventas/<uuid:uuid>/',
         PreventaDetailView.as_view(), name='preventa-detail'),
    path('preventas/<uuid:uuid>/status/',
         PreventaUpdateStatusView.as_view(), name='preventa-update-status'),

]
