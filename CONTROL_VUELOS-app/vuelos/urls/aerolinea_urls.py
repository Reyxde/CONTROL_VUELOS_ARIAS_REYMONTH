from django.urls import path

from vuelos.views.aerolinea_views import (
    home, aerolinea_list, aerolinea_detail, aerolinea_create,
    aerolinea_update, aerolinea_delete,
)

urlpatterns = [
    path('', home, name='home'),
    path('aerolineas/', aerolinea_list, name='aerolinea_list'),
    path('aerolineas/nuevo/', aerolinea_create, name='aerolinea_create'),
    path('aerolineas/<int:pk>/', aerolinea_detail, name='aerolinea_detail'),
    path('aerolineas/<int:pk>/editar/', aerolinea_update, name='aerolinea_update'),
    path('aerolineas/<int:pk>/eliminar/', aerolinea_delete, name='aerolinea_delete'),
]
