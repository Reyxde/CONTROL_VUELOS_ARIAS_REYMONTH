from django.urls import path

from vuelos.views.pasajero_views import (
    pasajero_list, pasajero_detail, pasajero_create, pasajero_update, pasajero_delete)

urlpatterns = [
    path('pasajeros/', pasajero_list, name='pasajero_list'),
    path('pasajeros/nuevo/', pasajero_create, name='pasajero_create'),
    path('pasajeros/<int:pk>/', pasajero_detail, name='pasajero_detail'),
    path('pasajeros/<int:pk>/editar/', pasajero_update, name='pasajero_update'),
    path('pasajeros/<int:pk>/eliminar/', pasajero_delete, name='pasajero_delete'),
]
